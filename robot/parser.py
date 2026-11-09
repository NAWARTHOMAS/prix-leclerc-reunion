import re
from typing import Optional, Tuple

_UNIT_RE = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*€\s*/\s*(\S+)?\s*$")


def parse_unit_price(text: str) -> Tuple[Optional[float], Optional[str]]:
    """'9.58 € / kg' -> (9.58, 'kg'). Valeur invalide ('INF € /') -> (None, None)."""
    match = _UNIT_RE.match(text or "")
    if not match:
        return (None, None)
    value = float(match.group(1).replace(",", "."))
    label = match.group(2)
    return (value, label.lower() if label else None)
