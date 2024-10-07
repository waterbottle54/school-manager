from enum import Enum


class SORT(Enum):
    ELEMENTARY = 0
    MIDDLE = 1
    HIGH = 2


def get_school_sort(title: str) -> SORT | None:
    if len(title) <= 1:
        return None
    if title[-1] == "초":
        return SORT.ELEMENTARY
    if title[-1] == "중":
        return SORT.MIDDLE
    if title[-1] == "고":
        return SORT.HIGH
    if "초교" in title or "초등" in title or "초등학교" in title:
        return SORT.ELEMENTARY
    if "중학" in title or "중학교" in title or "중교" in title:
        return SORT.MIDDLE
    if "고교" in title or "고등" in title or "고등학교" in title:
        return SORT.HIGH
    return None
