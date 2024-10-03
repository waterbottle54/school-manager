from data.common.JsonStream import *


class DictOfListRepository[T]:

    def __init__(self, file_path):
        super().__init__()
        self.stream = JsonStream(file_path)

    def get_dict(self) -> dict[T, list[str]]:
        _dict = self.stream.read()
        return _dict if _dict is not None else {}

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

    def delete_item(self, key: T, item: str):
        _list = self.get_list_by_key(key)
        if item in _list:
            _list.remove(item)
            self.set_list_with_key(key, _list)

    def move_item_left(self, key: T, index: int):
        if index > 0:
            _list = self.get_list_by_key(key)
            _list.insert(index - 1, _list[index])
            _list.pop(index + 1)
            self.set_list_with_key(key, _list)

    def move_item_right(self, key: T, index: int):
        _list = self.get_list_by_key(key)
        if index < len(_list) - 1:
            _list.insert(index + 1, _list[index])
            _list.pop(index)
            self.set_list_with_key(key, _list)
