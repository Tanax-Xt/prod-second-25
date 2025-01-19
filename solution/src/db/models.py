from typing import Any

from pyheck import snake
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @declared_attr
    @classmethod
    def __tablename__(cls) -> Any:
        return snake(cls.__name__)
