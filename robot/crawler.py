import re
import time
from typing import Callable, Dict, List, Tuple

from bs4 import BeautifulSoup

from .models import Product
from .parser import parse_products

BASE_URL = "https://www.drivezeclerc.re"


def discover_categories(home_html: str, store: str) -> List[Tuple[int, str]]:
    pattern = re.compile(rf"^/{re.escape(store)}/(\d+)-[a-z0-9-]+$")
    found: Dict[int, str] = {}
    for link in BeautifulSoup(home_html, "html.parser").select("a[href]"):
        href = link["href"]
        if href.startswith(BASE_URL):
            href = href[len(BASE_URL):]
        match = pattern.match(href)
        if match:
            found[int(match.group(1))] = href
    return sorted(found.items())


def crawl_store(
    store: str,
    categories: List[Tuple[int, str]],
    fetch: Callable[[str], str],
    sleep: Callable[[float], None] = time.sleep,
    delay: float = 1.5,
    max_pages: int = 40,
) -> List[Product]:
    products: Dict[int, Product] = {}
    requests_made = 0
    for category_id, path in categories:
        seen_in_category = set()
        for page_number in range(1, max_pages + 1):
            url_path = path if page_number == 1 else f"{path}?p={page_number}"
            if requests_made:
                sleep(delay)
            html = fetch(url_path)
            requests_made += 1
            items = parse_products(html, category_id)
            new_items = [p for p in items if p.id not in seen_in_category]
            if not new_items:
                break
            for product in new_items:
                seen_in_category.add(product.id)
                products.setdefault(product.id, product)
    return list(products.values())
