from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    description: str
    answer: str

class ChecklistBase(BaseModel):
    title: str
    questions: List[Question]

class ChecklistCreate(ChecklistBase):
    pass

class ChecklistUpdate(ChecklistBase):
    pass

class Checklist(ChecklistBase):
    id: int

    class Config:
        orm_mode = True
