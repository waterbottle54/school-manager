from data.common.ListRepository import *


class SchoolRepository(ListRepository):

    def __init__(self):
        super().__init__("school.json")
