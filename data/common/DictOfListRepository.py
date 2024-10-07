from typing import Callable, get_origin
from common.LiveData import LiveData, MutableLiveData
from data.common.JsonStream import *


class DictOfListRepository[T]:

    def __init__(self, file_path: str, key_from_str: Callable[[str], T]):
        super().__init__()
        self.stream = JsonStream(file_path)
        self.key_from_str = key_from_str
        self.livedata = MutableLiveData[dict[T, list[str]]](dict())
        self.update_livedata()

    def get_dict(self) -> dict[T, list[str]]:
        dict_raw = self.stream.read()
        if (dict_raw is None) and not isinstance(dict_raw, dict):
            return {}
        dict_converted: dict[T, list[str]] = {}
        for key, value in dict_raw.items():
            if isinstance(key, str) and isinstance(value, list):
                key_converted = self.key_from_str(key)
                dict_converted[key_converted] = value
        return dict_converted

    def get_dict_livedata(self) -> LiveData[dict[T, list[str]]]:
        return self.livedata

    def update_livedata(self):
        self.livedata.set_value(self.get_dict())

    def get_list_by_key(self, key: T) -> list[str]:
        _dict = self.get_dict()
        return _dict[key] if key in _dict else []

    def set_list_with_key(self, key: T, _list: list[str]):
        _dict = self.get_dict()
        _dict[key] = _list
        self.stream.write(_dict)

    def insert_item(self, key: T, item: str, index: int = -1):
        _list = self.get_list_by_key(key)
        if item in _list:
            return
        if index != -1:
            _list.insert(index, item)
        else:
            _list.append(item)
        self.set_list_with_key(key, _list)
        self.update_livedata()

    def delete_item(self, key: T, item: str):
        _list = self.get_list_by_key(key)
        if item in _list:
            _list.remove(item)
            self.set_list_with_key(key, _list)
            self.update_livedata()

    def move_item_left(self, key: T, i: int):
        if i > 0:
            _list = self.get_list_by_key(key)
            _list[i], _list[i - 1] = _list[i - 1], _list[i]
            self.set_list_with_key(key, _list)
            self.update_livedata()

    def move_item_right(
        self,
        key: T,
        i: int,
    ):
        _list = self.get_list_by_key(key)
        if i < len(_list) - 1:
            _list[i], _list[i + 1] = _list[i + 1], _list[i]
            self.set_list_with_key(key, _list)
            self.update_livedata()
