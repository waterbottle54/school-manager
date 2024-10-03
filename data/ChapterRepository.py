from data.common.DictOfListRepository import *


class ChapterRepository(DictOfListRepository[int]):

    def __init__(self):
        super().__init__("chapter.json")
