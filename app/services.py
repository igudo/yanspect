from abstract import AbstractService, AbstractFactory
from dto import ImportsDto
from repositories import DBRepository
from models import ShopUnitType
from decorators import bool_on_error
from typing import List


class ImportsService(AbstractService):
    repository: DBRepository

    @bool_on_error
    def imports(self, dto: List[ImportsDto]) -> bool:
        for item in dto:
            self.repository.add_or_update(item)
        return True


class DeleteService(AbstractService):
    repository: DBRepository
    factory: AbstractFactory

    def __init__(self, factory, repository = None, client = None):
        self.factory = factory
        super().__init__(repository=repository, client=client)

    @bool_on_error
    def delete_category(self, item: ImportsDto) -> bool:
        for child_item in self.repository.select_items(parentId=item.id):
            child_item = self.factory.dict_to_dto(child_item)
            if child_item.type == ShopUnitType.CATEGORY:
                self.delete_category(child_item)
            else:
                self.delete_item(child_item)
        return self.repository.delete_category(item.id) == []

    @bool_on_error
    def delete_item(self, item: ImportsDto) -> bool:
        return self.repository.delete_item(item.id) == []

    @bool_on_error
    def get_item(self, id):
        return self.repository.get_item(id)