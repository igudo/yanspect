from typing import List
from pydantic import BaseModel
from enum import Enum


class ShopUnitType(str, Enum):
    CATEGORY = "CATEGORY"
    OFFER = "OFFER"


class ShopUnitImport(BaseModel):
    id: str
    name: str
    parentId: str = None
    type: ShopUnitType
    price: int = None

    class Config:
        use_enum_values = True


class ImportsRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: str
