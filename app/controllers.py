from abstract import AbstractController
from services import ImportsService, DeleteService, NodesService
from repositories import DBRepository
from factories import ImportsDtoFactory
from presenters import ImportsPresenter, NodesPresenter
from fastapi.exceptions import RequestValidationError
from exceptions import NotFoundException
from models import ImportsRequest, Error, StatusCode, ShopUnitType


class ImportsController(AbstractController):
    service = ImportsService
    factory = ImportsDtoFactory
    presenter = ImportsPresenter

    def __init__(self, db: DBRepository):
        service = self.service(repository=db)
        super().__init__(service=service)

    def import_items(self, model: ImportsRequest) -> str:
        try:
            dto = self.factory.model_to_dto(model)
        except ValueError as e:
            raise RequestValidationError(e)

        is_imported = self.service.imports(dto)
        return self.presenter.bool_to_response(is_imported)


class DeleteControlled(AbstractController):
    service = DeleteService
    factory = ImportsDtoFactory

    def __init__(self, db: DBRepository):
        service = self.service(self.factory, repository=db)
        super().__init__(service=service)

    def delete(self, id: str):
        item = self.service.repository.get_item(id)
        if type(item) != dict:
            raise NotFoundException(f"item with id {id} not found")
        dto = self.factory.dict_to_dto(item)
        if dto.type == ShopUnitType.CATEGORY:
            res = self.service.delete_category(dto)
        else:
            res = self.service.delete_item(dto)
        return ImportsPresenter.bool_to_response(res)


class NodesControlled(AbstractController):
    service = NodesService
    factory = ImportsDtoFactory
    presenter = NodesPresenter

    def __init__(self, db: DBRepository):
        service = self.service(self.presenter, repository=db)
        super().__init__(service=service)

    def nodes(self, id: str) -> dict:
        item = self.service.repository.get_item(id)
        if type(item) != dict:
            raise NotFoundException(f"item with id {id} not found")
        dto = self.factory.dict_to_dto(item)
        if dto.type == ShopUnitType.CATEGORY:
            res = self.service.category_nodes(dto)
        else:
            res = self.service.item_nodes(dto)
        return res
