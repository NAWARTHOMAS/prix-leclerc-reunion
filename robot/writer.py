import json
from datetime import datetime
from pathlib import Path
from typing import List

from .models import Product

SCHEMA_VERSION = 1


class SuspiciousDropError(RuntimeError):
    """Le nouveau fichier a beaucoup moins de produits que le précédent."""


def build_payload(store: str, products: List[Product], now: datetime) -> dict:
    ordered = sorted(products, key=lambda product: product.id)
    return {
        "schema_version": SCHEMA_VERSION,
        "store": store,
        "generated_at": now.isoformat(timespec="seconds"),
        "count": len(ordered),
        "products": [product.to_dict() for product in ordered],
    }


def write_store_file(out_dir, payload: dict, min_ratio: float = 0.5) -> Path:
    directory = Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{payload['store']}.json"
    if target.exists():
        previous = json.loads(target.read_text(encoding="utf-8")).get("count", 0)
        if previous and payload["count"] < previous * min_ratio:
            raise SuspiciousDropError(
                f"{payload['store']} : {payload['count']} produits contre {previous} "
                f"la fois précédente. Fichier non remplacé."
            )
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    temporary.replace(target)
    return target
