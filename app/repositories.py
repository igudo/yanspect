from abstract import AbstractRepository
from clients import PostgresClient
from dto import ImportsDto
import logging

logger = logging.getLogger(__name__)


class DBRepository(AbstractRepository, PostgresClient):
    def dump_link(self, dto: ImportsDto) -> bool:
        return self._dump()
