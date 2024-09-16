from data.common.JsonStream import *

class ListDictRepository:

    stream: JsonStream

    def __init__(self, file_path):
        super().__init__()
        self.stream = JsonStream(file_path)

    def get_dict(self) -> dict:
        _dict = self.stream.read()
        return _dict if _dict is not None else {}
    
    def get_list(self, key) -> list:
        key = str(key)
        _dict = self.get_dict()
        return _dict[key] if key in _dict else []
    
    def set_list(self, key, list) -> list:
        key = str(key)
        _dict = self.get_dict()
        _dict[key] = list
        self.stream.write(_dict)
    
    def insert_item(self, key, item, index = -1):
        key = str(key)
        _dict = self.get_dict()
        _list: list = self.get_list(key)
        if item not in _list:
            if index != -1:
                _list.insert(index, item)
            else:
                _list.append(item)
            _dict[key] = _list
            self.stream.write(_dict)
        
    def delete_item(self, key, item):
        key = str(key)
        _dict = self.get_dict()
        _list: list = self.get_list(key)
        if item in _list:
            _list.remove(item)
            _dict[key] = _list
            self.stream.write(_dict)

    def move_item_up(self, key, index):
        if index >= 1:
            key = str(key)
            _dict = self.get_dict()
            _list: list = self.get_list(key)
            copy = _list[index]
            _list.pop(index)
            _list.insert(index - 1, copy)
            _dict[key] = _list
            self.stream.write(_dict)

    def move_item_down(self, key, index):
        key = str(key)
        _dict = self.get_dict()
        _list: list = self.get_list(key)
        if index < len(_list) - 1:
            copy = _list[index]
            _list.pop(index)
            _list.insert(index + 1, copy)
            _dict[key] = _list
            self.stream.write(_dict)