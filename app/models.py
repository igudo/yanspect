from typing import List
from pydantic import BaseModel
from enum import Enum
from uuid import UUID


class ShopUnitType(str, Enum):
    """Тип элемента - категория или товар"""
    CATEGORY = "CATEGORY"
    OFFER = "OFFER"


class StatusCode(int, Enum):
    """Возвращаемые коды"""
    OK_200 = 200
    BAD_REQUEST_400 = 400
    NOT_FOUND_404 = 404


class ShopUnitImport(BaseModel):
    """Модель товара/категории при запросе /import"""
    id: UUID
    name: str
    parentId: UUID = None
    type: ShopUnitType
    price: int = None

    class Config:
        use_enum_values = True  # нужно для поддержки ShopUnitType, который Enum


class ImportsRequest(BaseModel):
    """Модель запроса /import"""
    items: List[ShopUnitImport]
    updateDate: str


class Error(BaseModel):
    """Формат возвращаемых ошибок"""
    code: int
    message: str


class ResponseContent(Error):
    """Формат возвращаемых ответов"""
    pass

