from abstract import AbstractService
from factories import ImportsDtoFactory
from dto import ImportsDto
from repositories import DBRepository
from models import ShopUnitType
from decorators import bool_on_error
from presenters import NodesPresenter
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
    @bool_on_error
    def delete(self, dto: ImportsDto) -> bool:
        if dto.type == ShopUnitType.CATEGORY:
            res = self.repository.delete_category(dto.id)
        else:
            res = self.repository.delete_item(dto.id)
        return res


class NodesService(AbstractService):
    repository: DBRepository
    presenter: NodesPresenter

    def __init__(self, presenter, repository = None, client = None):
        self.presenter = presenter
        super().__init__(repository=repository, client=client)

    @bool_on_error
    def category_nodes(self, dto: ImportsDto) -> dict:
        d = self.repository.get_item(dto.id)
        d = self.presenter.to_category_nodes_dict(d)
        for ch in self.repository.select_items(parentId=dto.id):
            if ch["type"] == ShopUnitType.CATEGORY:
                d["children"].append(self.category_nodes(ImportsDtoFactory.dict_to_dto(ch)))
            else:
                d["children"].append(self.item_nodes(ImportsDtoFactory.dict_to_dto(ch)))
        return d

    @bool_on_error
    def item_nodes(self, dto: ImportsDto) -> dict:
        d = self.repository.get_item(dto.id)
        return self.presenter.to_item_nodes_dict(d)

