from abc import ABC, ABCMeta
from typing import Union, Type, TypeVar
from pydantic import BaseModel
from models import StatusCode

TV = TypeVar('TV')

Service = Union[Type[TV], TV, None]
Factory = Union[Type[TV], TV, None]
Presenter = Union[Type[TV], TV, None]
Client = Union[Type[TV], TV, None]
Repository = Union[Type[TV], TV, None]


class AbstractClient(ABC):
    """Паттерн описывающий обращение к внешним сервисам"""
    pass


class AbstractRepository(ABC):
    """Паттерн описывающий обращение к источникам данных"""
    pass


class AbstractService(ABC):
    """Паттерн описывающий бизнес-логику"""
    repository: Repository = None
    client: Client = None

    def __init__(self, repository: Repository = None, client: Client = None):
        self.repository = repository
        self.client = client


class AbstractFactory(ABC):
    """Паттерн описывающий создание сложных объектов"""
    dto_class: Type[BaseModel]


class AbstractPresenter(ABC):
    """Паттерн описывающий отображение данных"""

    @classmethod
    def bool_to_response(cls, value: bool) -> str:
        result = StatusCode.OK_200 if value else StatusCode.BAD_REQUEST_400
        return str(result.value)


class AbstractController(ABC):
    """Паттерн описывающий сложное взаимодействие сервисов друг с другом"""
    service: Service = None
    factory: Factory = None
    presenter: Presenter = None

    def __init__(self, service: Service = None):
        self.service = service


class AbstractDBClient(AbstractClient, metaclass=ABCMeta):
    """Описывает метод инициализации для всех DataBase Client"""
    connect: callable

    def __init__(self, host: str, database_name: str, user: str, password: str):
        self.connect(host, database_name, user, password)