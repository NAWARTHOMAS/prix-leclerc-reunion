import argparse
import os
import sys
import time
from datetime import datetime, timezone

from .crawler import crawl_store, discover_categories
from .fetcher import Fetcher
from .writer import build_payload, write_store_file

STORES = ["riviere-des-pluies"]


def run_store(store, fetch, out_dir, now, sleep=time.sleep, max_categories=None) -> int:
    home_html = fetch(f"/{store}/")
    categories = discover_categories(home_html, store)
    if max_categories:
        categories = categories[:max_categories]
    products = crawl_store(store, categories, fetch, sleep=sleep)
    payload = build_payload(store, products, now)
    write_store_file(out_dir, payload)
    return payload["count"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Robot de prix Leclerc Réunion")
    parser.add_argument("--store", action="append", choices=STORES)
    parser.add_argument("--out", default="data")
    parser.add_argument("--max-categories", type=int, default=None)
    args = parser.parse_args(argv)

    fetch = Fetcher(contact=os.environ.get("ROBOT_CONTACT", ""))
    failures = 0
    for store in args.store or STORES:
        try:
            count = run_store(
                store,
                fetch,
                args.out,
                datetime.now(timezone.utc),
                max_categories=args.max_categories,
            )
            print(f"{store} : {count} produits")
        except Exception as error:  # un magasin en échec ne bloque pas les autres
            failures += 1
            print(f"{store} : ÉCHEC - {error}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
