from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from models import ShopUnitType


class Dto(ABC):
    """Data transfer object"""
    pass


@dataclass(frozen=True)
class ImportsDto(Dto):
    """Объект """
    id: str
    name: str
    type: ShopUnitType
    update_date: datetime
    price: int = None
    parentId: str = None


