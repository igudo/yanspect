from abstract import AbstractRepository
from clients import PostgresClient
from dto import ImportsDto
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

    def add_or_update(self, dto: ImportsDto) -> bool:
        tn = self.categories_table_name if dto.type == ShopUnitType.CATEGORY else self.offers_table_name
        item = self.select(tn, id=dto.id)
        if item:
            if self.tuple_to_dict(item)["update_date"] < dto.update_date:
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
        return True

    def get_item(self, id: str) -> dict:
        for tn in (self.offers_table_name, self.categories_table_name):
            el = self.select(tn, id=id)
            if el:
                ell = self.tuple_to_dict(el[0])
                if tn == self.categories_table_name:
                    ell["type"] = ShopUnitType.CATEGORY
                else:
                    ell["type"] = ShopUnitType.OFFER
                return ell

    def select_items(self, **kwargs) -> List[dict]:
        l = []
        for tn in (self.offers_table_name, self.categories_table_name):
            els = self.select(tn, **kwargs)
            for el in els:
                ell = self.tuple_to_dict(el)
                if tn == self.categories_table_name:
                    ell["type"] = ShopUnitType.CATEGORY
                else:
                    ell["type"] = ShopUnitType.OFFER
                l.append(ell)
        return l

    def delete_category(self, id: str):
        return self.delete(self.categories_table_name, id)

    def delete_item(self, id: str):
        return self.delete(self.offers_table_name, id)

    def create_tables(self):
        self.create_table_if_not_exists(self.offers_table_name, self.schema)
        self.create_table_if_not_exists(self.categories_table_name, self.schema)

    def tuple_to_dict(self, t):
        return {
            "id": t[0],
            "parentId": t[1],
            "name": t[2],
            "update_date": t[3],
            "price": t[4]
        }

    def close(self):
        self.db.close()

