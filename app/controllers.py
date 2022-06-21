from abstract import AbstractController
from services import ImportsService
from models import ImportsRequest
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