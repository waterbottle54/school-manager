from data.ProblemHeader import *

def grade_name(grade: int):
    if grade < 0 or grade > 11:
        return '-'
    table = [ '초1', '초2', '초3', '초4', '초5', '초6', '중1', '중2', '중3', '고1', '고2', '고3' ]
    return table[grade]

def problem_title(header: ProblemHeader):
    return f"{header.book} {grade_name(header.grade)}-{header.chapter} prob.{header.title}"
