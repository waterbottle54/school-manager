from abc import ABC, abstractmethod
import typing


class DataObject[T](ABC):

    @abstractmethod
    def to_record(self) -> dict[str, object]: ...

    @staticmethod
    @abstractmethod
    def from_record(record: list[T]): ...

    @staticmethod
    def cast[_T](value: object, _type: type[_T]) -> _T:
        if isinstance(value, _type):
            return value
        else:
            raise Exception(f"value of type {_type} is not of type {_type}")
