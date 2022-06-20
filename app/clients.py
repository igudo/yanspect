from typing import Any
from abstract import AbstractDBClient
import psycopg2
import logging

logger = logging.getLogger(__name__)


class PostgresClient(AbstractDBClient):
    db: psycopg2._psycopg.connection

    def connect(self, host, database_name, user, password, port):
        self.db = psycopg2.connect(dbname=database_name, user=user, password=password, host=host, port=port)

    def _execute(self, cmd) -> list:
        cursor = self.db.cursor()
        cursor.execute(cmd)
        try:
            d = cursor.fetchall()
        except psycopg2.ProgrammingError:
            d = []
        cursor.close()
        return d

    def create_table_if_not_exists(self, table_name, schema):
        self._execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
          {schema}
        );
        """)


