from data.common.ListRepository import *

class BookRepository(ListRepository):

    def __init__(self):
        super().__init__("book.json")