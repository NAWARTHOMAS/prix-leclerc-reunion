import re
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup

from .models import Product

_UNIT_RE = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*€\s*/\s*(\S+)?\s*$")


def parse_unit_price(text: str) -> Tuple[Optional[float], Optional[str]]:
    """'9.58 € / kg' -> (9.58, 'kg'). Valeur invalide ('INF € /') -> (None, None)."""
    match = _UNIT_RE.match(text or "")
    if not match:
        return (None, None)
    value = float(match.group(1).replace(",", "."))
    label = match.group(2)
    return (value, label.lower() if label else None)


def parse_products(html: str, category_id: int) -> List[Product]:
    soup = BeautifulSoup(html, "html.parser")
    products: List[Product] = []
    for item in soup.select("li.ajax_block_product"):
        button = item.select_one("[data-id-product]")
        link = item.select_one("a.product-name")
        price_meta = item.select_one("meta[itemprop=price]")
        if not (button and link and price_meta):
            continue
        try:
            product_id = int(button["data-id-product"])
            price = float(price_meta["content"])
        except (KeyError, ValueError):
            continue
        unit_box = item.select_one(".grid-left-bottom strong")
        unit_price, unit_label = parse_unit_price(
            unit_box.get_text(" ", strip=True) if unit_box else ""
        )
        availability = item.select_one("link[itemprop=availability]")
        in_stock = bool(availability and "InStock" in availability.get("href", ""))
        products.append(
            Product(
                id=product_id,
                name=link.get_text(strip=True),
                price=price,
                unit_price=unit_price,
                unit_label=unit_label,
                in_stock=in_stock,
                category_id=category_id,
                url=link.get("href", ""),
            )
        )
    return products
