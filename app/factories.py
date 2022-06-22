from typing import List
from abstract import AbstractFactory
from dto import ImportsDto
from datetime import datetime
from models import ImportsRequest


class ImportsDtoFactory(AbstractFactory):
    dto_class = ImportsDto

    @classmethod
    def model_to_dto(cls, model: ImportsRequest) -> List[ImportsDto]:
        d = []
        for item in model.items:
            d.append(cls.dto_class(
                name=item.name,
                id=item.id,
                type=item.type,
                price=item.price,
                parentId=item.parentId,
                update_date=datetime.strptime(model.updateDate, "%Y-%m-%dT%H:%M:%S.%fZ")
            ))
        return d

    @classmethod
    def dict_to_dto(cls, d: dict) -> ImportsDto:
        return cls.dto_class(
            name=d["name"],
            id=d["id"],
            type=d["type"],
            price=d["price"],
            parentId=d["parentId"],
            update_date=d["update_date"]
        )
