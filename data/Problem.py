from time import time
import json

from data.common.DataObject import *


class Problem(DataObject["Problem"]):

    def __init__(
        self,
        grade: int,
        chapter: str,
        book: str,
        title: str,
        num_choice: int,
        ans_msq: list[int],
        ans_saq: dict[int, str],
        id=-1,
        created=-1,
    ):
        self.id = id
        self.grade = grade
        self.chapter = chapter
        self.book = book
        self.title = title
        self.num_choice = num_choice
        self.ans_mcq = ans_msq
        self.ans_saq = ans_saq
        self.created = created if created != -1 else int(time())

    def to_record(self) -> dict[str, object]:
        return {
            "p_id": self.id,
            "grade": self.grade,
            "chapter": self.chapter,
            "book": self.book,
            "title": self.title,
            "num_choice": self.num_choice,
            "ans_mcq": json.dumps(self.ans_mcq),
            "ans_saq": Problem.ans_saq_to_json(self.ans_saq),
            "created": self.created,
        }

    @staticmethod
    def from_record(record: list[object]) -> "Problem":
        id = DataObject.cast(record[0], int)
        grade = DataObject.cast(record[1], int)
        chapter = DataObject.cast(record[2], str)
        book = DataObject.cast(record[3], str)
        title = DataObject.cast(record[4], str)
        num_choice = DataObject.cast(record[5], int)
        json_ans_mcq = DataObject.cast(record[6], str)
        json_ans_saq = DataObject.cast(record[7], str)
        created = DataObject.cast(record[8], int)

        ans_mcq = json.loads(json_ans_mcq)
        ans_saq = Problem.and_saq_from_json(json_ans_saq)
        return Problem(
            grade, chapter, book, title, num_choice, ans_mcq, ans_saq, id, created
        )

    @staticmethod
    def ans_saq_to_json(_ans_saq: dict[int, str]) -> str:
        ans_saq = _ans_saq.copy()
        for key, answer in ans_saq.items():
            answer: str
            answer = answer.replace(",", "#comma#").replace(":", "#colon#")
            ans_saq[key] = answer
        return json.dumps(ans_saq)

    @staticmethod
    def and_saq_from_json(_json: str) -> dict[int, str]:
        ans_saq = json.loads(_json)
        if not isinstance(ans_saq, dict):
            raise Exception(
                f"Cannot convert json string into dict[int, str]: check {_json}"
            )
        for key, answer in ans_saq.items():
            answer: str
            answer = answer.replace("#comma#", ",").replace("#colon#", ":")
            ans_saq[key] = answer
        return ans_saq
