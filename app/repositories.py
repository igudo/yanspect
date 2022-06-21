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
        if self.select(tn, id=dto.id):
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
        print(self.select(self.categories_table_name))
        print(self.select(self.offers_table_name))
        return True

    def create_tables(self):
        self.create_table_if_not_exists(self.offers_table_name, self.schema)
        self.create_table_if_not_exists(self.categories_table_name, self.schema)

