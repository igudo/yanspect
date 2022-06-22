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

    @classmethod
    def make_category_price(cls, d: dict) -> tuple:
        p = 0
        i = 0
        for ch in d["children"]:
            if ch["type"] == ShopUnitType.CATEGORY:
                p1,i1 = cls.make_category_price(ch)
                p+=p1
                i+=i1
            else:
                i+=1
                p+=ch["price"]
        if i==0:
            d["price"] = None
        else:
            d["price"] = int(p/i)
        return p,i
