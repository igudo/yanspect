from abstract import AbstractRepository
from clients import PostgresClient
from dto import ImportsDto
import logging

logger = logging.getLogger(__name__)


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
        d = self._execute(f"SELECT * FROM {self.categories_table_name};")
        print(d)
        return True

    def create_tables(self):
        self.create_table_if_not_exists(self.offers_table_name, self.schema)
        self.create_table_if_not_exists(self.categories_table_name, self.schema)
