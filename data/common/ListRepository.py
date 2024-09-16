from data.common.JsonStream import *

class ListRepository:

    stream: JsonStream

    def __init__(self, file_path):
        super().__init__()
        self.stream = JsonStream(file_path)

    def get_list(self) -> list:
        list = self.stream.read()
        return list if list is not None else []

    def add_item(self, new_item):
        _list: list = self.get_list()
        if new_item not in _list:
            _list.append(new_item)
            self.stream.write(_list)
        
    def delete_item(self, item):
        _list: list = self.get_list()
        if item in _list:
            _list.remove(item)
            self.stream.write(_list)