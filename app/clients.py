from typing import Any
from abstract import AbstractDBClient
import psycopg2
import logging

logger = logging.getLogger(__name__)


class PostgresClient(AbstractDBClient):
    db: psycopg2._psycopg.connection

    def connect(self, host, database_name, user, password):
        self.db = psycopg2.connect(dbname=database_name, user=user, password=password, host=host)

    def _dump(self) -> bool:
        cursor = self.db.cursor()
        cursor.close()
        return True

    def _query(self, field: str) -> Any:
        return True

