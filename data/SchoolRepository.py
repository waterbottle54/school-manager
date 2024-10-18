from data.common.ListRepository import *


class SchoolRepository(ListRepository):

    _instance: "SchoolRepository | None" = None

    @staticmethod
    def get_instance() -> "SchoolRepository":
        if SchoolRepository._instance is None:
            SchoolRepository._instance = SchoolRepository()
        return SchoolRepository._instance

    def __init__(self):
        super().__init__("school.json")
