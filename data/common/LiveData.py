from operator import call
from typing import Callable, TypeVar

from ui.common.Fragment import Fragment


T = TypeVar("T")  # Define the type variable


class Observer[T]:

    def __init__(self, callback: Callable[[T], None], fragment: Fragment | None = None):
        self.callback = callback
        self.fragment = fragment


class LiveData[T]:

    def __init__(self, value: T):
        self.value = value
        self.observers = list[Observer]()

    def _set_value(self, value: T):
        self.value = value
        for observer in self.observers:
            if observer.fragment:
                observer.fragment.block_all_signals(True)
            observer.callback(self.value)
            if observer.fragment:
                observer.fragment.block_all_signals(False)

    def _publish(self):
        self._set_value(self.value)

    def _observe(self, callback: Callable[[T], None]):
        self.observers.append(Observer(callback, None))

    # observation from fragment (UI)
    def observe(self, fragment: Fragment, callback: Callable[[T], None]):
        self.observers.append(Observer(callback, fragment))
        fragment.observe_resume(lambda: self._publish())


class MutableLiveData[T](LiveData[T]):
    def __init__(self, value: T):
        super().__init__(value)

    def set_value(self, value: T):
        super()._set_value(value)

    def publish(self):
        super()._publish()


def map[S, T](source: LiveData[S], t: Callable[[S], T]) -> LiveData[T]:
    data = LiveData(t(source.value))
    source._observe(lambda value: data._set_value(t(value)))
    return data


def map2[
    S1, S2, T
](s1: LiveData[S1], s2: LiveData[S2], t: Callable[[S1, S2], T]) -> LiveData[T]:
    data = LiveData(t(s1.value, s2.value))
    s1._observe(lambda value: data._set_value(t(value, s2.value)))
    s2._observe(lambda value: data._set_value(t(s1.value, value)))
    return data


def map3[
    S1, S2, S3, T
](
    s1: LiveData[S1], s2: LiveData[S2], s3: LiveData[S3], t: Callable[[S1, S2, S3], T]
) -> LiveData[T]:
    data = LiveData(t(s1.value, s2.value, s3.value))
    s1._observe(lambda value: data._set_value(t(value, s2.value, s3.value)))
    s2._observe(lambda value: data._set_value(t(s1.value, value, s3.value)))
    s3._observe(lambda value: data._set_value(t(s1.value, s2.value, value)))
    return data


def map4[
    S1, S2, S3, S4, T
](
    s1: LiveData[S1],
    s2: LiveData[S2],
    s3: LiveData[S3],
    s4: LiveData[S4],
    t: Callable[[S1, S2, S3, S4], T],
) -> LiveData[T]:
    data = LiveData(t(s1.value, s2.value, s3.value, s4.value))
    s1._observe(lambda value: data._set_value(t(value, s2.value, s3.value, s4.value)))
    s2._observe(lambda value: data._set_value(t(s1.value, value, s3.value, s4.value)))
    s3._observe(lambda value: data._set_value(t(s1.value, s2.value, value, s4.value)))
    s4._observe(lambda value: data._set_value(t(s1.value, s2.value, s3.value, value)))
    return data
