from typing import Optional
from abstract import AbstractFactory
from dto import ImportsDto
from models import ImportsRequest


class ImportsDtoFactory(AbstractFactory):
    dto_class = ImportsDto

    @classmethod
    def model_to_dto(cls, model: ImportsRequest):
        return cls.dto_class()

