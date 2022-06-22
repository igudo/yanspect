from abstract import AbstractController
from services import ImportsService, DeleteService
from models import ImportsRequest, ShopUnitType
from repositories import DBRepository
from factories import ImportsDtoFactory
from presenters import ImportsPresenter
from fastapi.exceptions import RequestValidationError, ValidationError


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

    def delete(self, id: str) -> str:
        item = self.service.get_item(id)
        if type(item) != dict:
            raise RequestValidationError("Bad request")
        dto = self.factory.dict_to_dto(item)
        if dto.type == ShopUnitType.CATEGORY:
            res = self.service.delete_category(dto)
        else:
            res = self.service.delete_item(dto)
        return ImportsPresenter.bool_to_response(res)
