from abstract import AbstractController
from services import ImportsService, DeleteService, NodesService, SalesService
from repositories import DBRepository
from factories import ImportsDtoFactory
from presenters import ImportsPresenter, NodesPresenter
from fastapi.exceptions import RequestValidationError
from exceptions import NotFoundException
from datetime import datetime
from uuid import UUID
from typing import Union
from models import ImportsRequest, Error, StatusCode, ShopUnitType


class ImportsController(AbstractController):
    service = ImportsService
    factory = ImportsDtoFactory
    presenter = ImportsPresenter

    def __init__(self, db: DBRepository):
        service = self.service(repository=db)
        super().__init__(service=service)

    def import_items(self, model: ImportsRequest) -> bool:
        try:
            dto = self.factory.model_to_dto(model)
        except ValueError as e:
            raise RequestValidationError(e)
        return self.service.imports(dto)


class DeleteController(AbstractController):
    service = DeleteService
    factory = ImportsDtoFactory

    def __init__(self, db: DBRepository):
        service = self.service(repository=db)
        super().__init__(service=service)

    def delete(self, id: str) -> bool:
        try:
            if str(UUID(id)) != id:
                raise ValueError("wrong id format")
        except ValueError as e:
            raise RequestValidationError(e)
        item = self.service.repository.get_item(id)
        if type(item) != dict:
            raise NotFoundException(f"item with id {id} not found")
        dto = self.factory.dict_to_dto(item)
        return self.service.delete(dto)


class NodesController(AbstractController):
    service = NodesService
    factory = ImportsDtoFactory
    presenter = NodesPresenter

    def __init__(self, db: DBRepository):
        service = self.service(self.presenter, repository=db)
        super().__init__(service=service)

    def nodes(self, id: str) -> Union[dict, bool]:
        try:
            if str(UUID(id)) != id:
                raise ValueError("wrong id format")
        except ValueError as e:
            raise RequestValidationError(e)
        item = self.service.repository.get_item(id)
        if type(item) != dict:
            raise NotFoundException(f"item with id {id} not found")
        dto = self.factory.dict_to_dto(item)
        if dto.type == ShopUnitType.CATEGORY:
            res = self.service.category_nodes(dto)
        else:
            res = self.service.item_nodes(dto)
        return res

    def statistic(self, id: str, dateStart: str, dateEnd: str) -> Union[bool, dict]:
        try:
            if str(UUID(id)) != id:
                raise ValueError("wrong id format")
        except ValueError as e:
            raise RequestValidationError(e)
        try:
            date1 = datetime.strptime(dateStart, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError as e:
            raise RequestValidationError(e)
        try:
            date2 = datetime.strptime(dateEnd, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError as e:
            raise RequestValidationError(e)

        item = self.service.repository.get_item(id)
        if type(item) != dict:
            raise NotFoundException(f"item with id {id} not found")

        r = self.service.statistic(id, date1, date2)
        if type(r) != list:
            return False
        return {"items": r}


class SalesController(AbstractController):
    service = SalesService

    def __init__(self, db: DBRepository):
        service = self.service(repository=db)
        super().__init__(service=service)

    def sales(self, date: str) -> Union[bool, dict]:
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError as e:
            raise RequestValidationError(e)
        r = self.service.sales(date)
        if type(r) != list:
            return False
        return {"items": r}
