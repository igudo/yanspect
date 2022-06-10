from abstract import AbstractService
from dto import ImportsDto
from repositories import DBRepository
from decorators import bool_on_error


class ImportsService(AbstractService):
    repository: DBRepository

    @bool_on_error
    def imports(self, dto: ImportsDto):
        self.repository.dump_link(dto)
        return True