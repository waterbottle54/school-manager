from data.common.ListDictRepository import *

class ChapterRepository(ListDictRepository):

    def __init__(self):
        super().__init__("chapter.json")