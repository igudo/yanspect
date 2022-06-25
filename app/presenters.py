from models import ShopUnitType
from abstract import AbstractPresenter


class ImportsPresenter(AbstractPresenter):
    pass

class NodesPresenter(AbstractPresenter):
    @classmethod
    def to_item_nodes_dict(cls, d) -> dict:
        d = cls.to_category_nodes_dict(d)
        d["children"] = None
        return d

    @classmethod
    def to_category_nodes_dict(cls, d: dict) -> dict:
        d["children"] = []
        d["date"] = d["update_date"].isoformat(timespec='milliseconds')+"Z"
        del d["update_date"]
        return d
