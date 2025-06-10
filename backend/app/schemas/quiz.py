from pydantic import BaseModel
from typing import List

class ChoicesOut(BaseModel):
    ChoiceText: str
    IsTrue: bool

class QuestionOut(BaseModel):
    QuestionNumber: int
    QuestionText: str
    QuestionPoint: int
    Choices: list[ChoicesOut]

class QuizBase(BaseModel):
    QuizName: str
    TimeTaken: int
    NumQuestions: int
    QuizPoint: int

class QuizCreate(QuizBase):
    pass

class QuizOut(QuizBase):
    ClassID: int
    Questions: List[QuestionOut]

    class Config:
        orm_mode = True
