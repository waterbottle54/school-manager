from common.LiveData import LiveData, MutableLiveData
from data.common.JsonStream import *


class ListRepository:

    def __init__(self, file_path):
        super().__init__()
        self.stream = JsonStream(file_path)
        self.livedata = MutableLiveData[list[str]]([])
        self.update_livedata()

    def get_list(self) -> list[str]:
        list = self.stream.read()
        return list if list is not None else []

    def get_list_livedata(self) -> LiveData[list[str]]:
        return self.livedata

    def update_livedata(self):
        self.livedata.set_value(self.get_list())

    def add_item(self, item: str):
        _list: list[str] = self.get_list()
        if item not in _list:
            _list.append(item)
            self.stream.write(_list)
            self.update_livedata()

    def delete_item(self, item: str):
        _list: list = self.get_list()
        if item in _list:
            _list.remove(item)
            self.stream.write(_list)
            self.update_livedata()
