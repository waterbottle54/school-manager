import select
from typing import Callable
from data.common.LiveData import LiveData, MutableLiveData, map2


class LiveList[T]:
    """_summary_
    This class provides selection functionality for the LiveData that holds python list (of type T).
    It manages selection status of the list, and provides interface to selection status.
    * IMPORTANT: Do not change current selection outside the class during data manipulation (CRUD),
    because the order of outer request and automatic request by the data manipulation will become unexpectable.
    (Remember that you might have to update list/table widget's selection unsyncronously)
    """

    def __init__(
        self,
        livedata: LiveData[list[T]],
    ):
        super().__init__()
        self._lst = livedata
        self._idx = MutableLiveData[int](-1)
        self._cur = map2(
            self._lst,
            self._idx,
            lambda list, i: list[i] if (i >= 0) and (i <= len(list) - 1) else None,
        )
        self._get_default_index_on_update: Callable[[list[T], int, int], int] | None = (
            None
        )
        self._is_get_default_one_shot: bool = True
        self._lst._observe(self.on_list_data_changed)

    def on_list_data_changed(self, lst: list[T]):
        current_index = self._idx.value
        if self._get_default_index_on_update is None:
            self.select_at(current_index)
        else:
            new_index = self._get_default_index_on_update(
                lst,
                self.size() - 1,
                current_index,
            )
            self.select_at(new_index)
            if self._is_get_default_one_shot:
                self._get_default_index_on_update = None

    def has_selection(self):
        return self._cur.value is not None

    def size(self) -> int:
        return len(self._lst.value)

    def list_livedata(self) -> LiveData[list[T]]:
        return self._lst

    def index_livedata(self) -> LiveData[int]:
        return self._idx

    def selected_livedata(self) -> LiveData[T | None]:
        return self._cur

    def list_value(self) -> list[T]:
        return self._lst.value

    def index_value(self) -> int:
        return self._idx.value

    def selected_value(self) -> T | None:
        return self._cur.value

    def get_at(self, i: int) -> T | None:
        lst = self._lst.value
        return lst[i] if (i >= 0) and (i <= len(lst) - 1) else None

    def select_at(self, index: int):
        if (index < 0) or (index > len(self._lst.value) - 1):
            self._idx.set_value(-1)
        else:
            self._idx.set_value(index)

    def select_end(self):
        self._idx.set_value(len(self._lst.value) - 1)

    def select(self, value: T):
        lst = self._lst.value
        if len(lst) == 0:
            self._idx.set_value(-1)
            return
        try:
            index = lst.index(value)
            self._idx.set_value(index)
        except ValueError:
            self._idx.set_value(-1)

    def select_if(self, condition: Callable[[T], bool]):
        for i, elem in enumerate(self._lst.value):
            if condition(elem):
                self.select(elem)
                return

    def unselect(self):
        self._idx.set_value(-1)

    def set_default_index_on_update(
        self, is_one_shot: bool, get_default_index: Callable[[list[T], int, int], int]
    ):
        self._get_default_index_on_update = get_default_index
        self._is_get_default_one_shot = is_one_shot

    def remove_default_index_on_update(self):
        self._get_default_index_on_update = None


class MutableLiveList[T](LiveList[T]):

    def __init__(self, value: list[T]):
        super().__init__(MutableLiveData(value))

    def set_list(self, data: list[T]):
        if isinstance(self._lst, MutableLiveData):
            self._lst._set_value(data)
