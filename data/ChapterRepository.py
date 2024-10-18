from data.common.DictOfListRepository import *


class ChapterRepository(DictOfListRepository[int]):

    _instance: "ChapterRepository | None" = None

    @staticmethod
    def get_instance() -> "ChapterRepository":
        if ChapterRepository._instance is None:
            ChapterRepository._instance = ChapterRepository()
        return ChapterRepository._instance

    def __init__(self):
        super().__init__("chapter.json", int)
