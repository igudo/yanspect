from abstract import AbstractRepository
from clients import PostgresClient
from dto import ImportsDto
from factories import ImportsDtoFactory
from models import ShopUnitType
from typing import List


class DBRepository(AbstractRepository, PostgresClient):
    offers_table_name: str
    categories_table_name: str
    schema = """
        id varchar(36) NOT NULL,
        parentId varchar(36),
        name varchar(450) NOT NULL,
        date timestamp NOT NULL,
        price integer,
        PRIMARY KEY (id)
    """

    def update_category_date(self, dto: ImportsDto):
        if dto.parentId:
            self.update(self.categories_table_name, dto.parentId, date=dto.update_date)
            self.update_category_date(ImportsDtoFactory.dict_to_dto(self.get_item(dto.parentId)))


    def add_or_update(self, dto: ImportsDto) -> bool:
        tn = self.categories_table_name if dto.type == ShopUnitType.CATEGORY else self.offers_table_name
        item = self.select(tn, id=dto.id)
        if item:
            if self.tuple_to_dict(item[0], tn)["update_date"] < dto.update_date:
                self.update(
                    tn,
                    dto.id,
                    name=dto.name,
                    parentId=dto.parentId,
                    date=dto.update_date,
                    price=dto.price
                )
        else:
            self.insert(
                tn,
                dto.id,
                dto.parentId,
                dto.name,
                dto.update_date,
                dto.price
            )
        self.update_category_date(dto)
        return True

    def get_item(self, id: str) -> dict:
        for tn in (self.offers_table_name, self.categories_table_name):
            el = self.select(tn, id=id)
            if el:
                ell = self.tuple_to_dict(el[0], tn)
                return ell

    def select_items(self, **kwargs) -> List[dict]:
        l = []
        for tn in (self.offers_table_name, self.categories_table_name):
            els = self.select(tn, **kwargs)
            for el in els:
                ell = self.tuple_to_dict(el, tn)
                l.append(ell)
        return l

    def delete_category(self, id: str):
        return self.delete(self.categories_table_name, id)

    def delete_item(self, id: str):
        return self.delete(self.offers_table_name, id)

    def create_tables(self):
        self.create_table_if_not_exists(self.offers_table_name, self.schema)
        self.create_table_if_not_exists(self.categories_table_name, self.schema)

    def tuple_to_dict(self, t: tuple, tname: str) -> dict:
        return {
            "id": t[0],
            "parentId": t[1],
            "name": t[2],
            "update_date": t[3],
            "price": t[4],
            "type": ShopUnitType.CATEGORY if tname==self.categories_table_name else ShopUnitType.OFFER
        }

    def close(self):
        self.db.close()

