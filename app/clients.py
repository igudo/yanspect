from typing import Any, List
from abstract import AbstractDBClient
import psycopg2
from datetime import datetime


class PostgresClient(AbstractDBClient):
    db: psycopg2._psycopg.connection

    def connect(self, host, database_name, user, password, port):
        """setup connection"""
        self.db = psycopg2.connect(dbname=database_name, user=user, password=password, host=host, port=port)
        self.db.autocommit = True

    def _execute(self, cmd) -> list:
        """execute a sql command
        returns list of response items"""
        cursor = self.db.cursor()
        cursor.execute(cmd)
        try:
            d = cursor.fetchall()
        except psycopg2.ProgrammingError:
            d = []
        cursor.close()
        return d

    def select(self, table_name, q="1=1", **kwargs) -> list:
        for k,v in kwargs.items():
            q+=f" AND {k}={self.e(v)}"
        return self._execute(f"SELECT * FROM {table_name} WHERE {q};")

    def insert(self, table_name, *args) -> list:
        return self._execute(f"INSERT INTO {table_name} VALUES ({','.join([str(self.e(arg)) for arg in args])});")

    def update(self, table_name, id, **kwargs) -> list:
        q = ",".join([f"{k}={self.e(v)}" for k,v in kwargs.items()])
        return self._execute(f"UPDATE {table_name} SET {q} WHERE id={self.e(id)};")

    def delete(self, table_name: str, id: str):
        return self._execute(f"DELETE FROM {table_name} WHERE id={self.e(id)};")

    def create_table_if_not_exists(self, table_name, schema):
        self._execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
          {schema}
        );
        """)

    def e(self, s):
        """escape string (экранировать строку)"""
        if type(s) == str:
            return "\'" + s + "\'"
        elif type(s) == int:
            return s
        elif type(s) == float:
            return int(s)
        elif type(s) == datetime:
            return f"TO_TIMESTAMP('{s.strftime('%Y-%m-%d %H:%M:%S.%f')}', 'YYYY-MM-DD HH24:MI:SS.FF')"
        else:
            return "null"


