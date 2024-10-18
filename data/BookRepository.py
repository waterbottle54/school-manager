from data.common.ListRepository import *


class BookRepository(ListRepository):

    _instance: "BookRepository | None" = None

    @staticmethod
    def get_instance() -> "BookRepository":
        if BookRepository._instance is None:
            BookRepository._instance = BookRepository()
        return BookRepository._instance

    def __init__(self):
        super().__init__("book.json")
