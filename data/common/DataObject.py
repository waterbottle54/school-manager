from abc import ABC, abstractmethod
from typing import cast


class DataObject[T](ABC):

    @abstractmethod
    def to_record(self) -> dict[str, object]: ...

    @staticmethod
    @abstractmethod
    def from_record(record: list[object]): ...

    @staticmethod
    def cast[_T](value: object, _type: type[_T]) -> _T:
        if type(value) is _type:
            return cast(_T, value)
        else:
            raise Exception(f"value of type {type(value)} is not of type {_type}")
