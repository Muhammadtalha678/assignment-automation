from pydantic import BaseModel

class data(BaseModel):
    assignment_no:int
    course_code:int
    semester:str
    student_name:str
    registration_id:int
    questions:list[str]
    language:str



class Section(BaseModel):
    heading:str
    explanation:str

class Question(BaseModel):
    question_number:int
    question_text:str
    introduction:str
    sections:list[Section]
    diagram_description:str
    conclusion:str
    
class Assignment(BaseModel):
    assignment_no:int
    course_code:int
    semester:str
    student_name:str
    registration_id:int
    questions:list[Question]