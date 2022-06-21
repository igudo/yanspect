from abstract import AbstractService
from dto import ImportsDto
from repositories import DBRepository
from decorators import bool_on_error
from typing import List


class ImportsService(AbstractService):
    repository: DBRepository

    @bool_on_error
    def imports(self, dto: List[ImportsDto]) -> bool:
        for item in dto:
            self.repository.add_or_update(item)
        return True