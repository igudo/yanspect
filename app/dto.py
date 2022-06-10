from abc import ABC
from dataclasses import dataclass
from typing import Optional


class Dto(ABC):
    """Data transfer object"""
    pass


@dataclass(frozen=True)
class ImportsDto(Dto):
    pass
