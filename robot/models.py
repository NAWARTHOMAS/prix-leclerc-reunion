from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price: float
    unit_price: Optional[float]
    unit_label: Optional[str]
    in_stock: bool
    category_id: int
    url: str

    def to_dict(self) -> dict:
        return asdict(self)
