from abstract import AbstractRepository
from clients import PostgresClient
from dto import ImportsDto
from factories import ImportsDtoFactory
from models import ShopUnitType
from typing import List, Tuple, Union


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

    def update_category(self, dto: ImportsDto, update_date=True) -> None:
        """Updates category price and date on child changing
        dto: ImportsDto of category child
        returns: None"""
        if dto.parentId:
            if update_date:
                self.update(self.categories_table_name, dto.parentId, date=dto.update_date)
            self.update_category_price(dto.parentId)
            self.update_category(ImportsDtoFactory.dict_to_dto(self.get_item(dto.parentId)), update_date=update_date)

    def update_category_price(self, id: str) -> Tuple[int, int]:
        """Updates category price
        id: id of category
        returns: (p, i)
        p: full price
        i: num of items"""
        p = 0
        i = 0
        chs = self.select_items(parentId=id)
        for ch in chs:
            if ch["type"] == ShopUnitType.CATEGORY:
                p1, i1 = self.update_category_price(ch["id"])
                p += p1
                i += i1
            else:
                i += 1
                p += ch["price"]
        if i == 0:
            self.update(self.categories_table_name, id, price=None)
        else:
            self.update(self.categories_table_name, id, price=int(p / i))
        return p, i

    def add_or_update(self, dto: ImportsDto) -> None:
        """Add new item or update if exists
        dto: new object data
        returns: None"""
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
        self.update_category(dto)

    def get_item(self, id: str) -> Union[dict, None]:
        """returns item by id
        id: get item with this id
        returns: dict of item values or None if not found"""
        items = self.select_items(id=id)
        if items:
            return items[0]

    def select_items(self, **kwargs) -> List[dict]:
        """get items filtering by kwargs"""
        l = []
        for tn in (self.offers_table_name, self.categories_table_name):
            els = self.select(tn, **kwargs)
            for el in els:
                ell = self.tuple_to_dict(el, tn)
                l.append(ell)
        return l

    def delete_category(self, id: str) -> bool:
        """delete category with id"""
        for child_item in self.select_items(parentId=id):
            child_item = ImportsDtoFactory.dict_to_dto(child_item)
            if child_item.type == ShopUnitType.CATEGORY:
                self.delete_category(child_item.id)
            else:
                self.delete_item(child_item.id)
        return self.delete(self.categories_table_name, id) == []

    def delete_item(self, id: str) -> bool:
        """delete item with id"""
        dto = ImportsDtoFactory.dict_to_dto(self.get_item(id))
        r = self.delete(self.offers_table_name, id)
        self.update_category(dto, update_date=False)
        return r == []

    def create_tables(self):
        """create tables via self.schema"""
        self.create_table_if_not_exists(self.offers_table_name, self.schema)
        self.create_table_if_not_exists(self.categories_table_name, self.schema)

    def tuple_to_dict(self, t: tuple, tname: str) -> dict:
        """tuple of cols from table to dictionary"""
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

