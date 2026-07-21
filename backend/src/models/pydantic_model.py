from pydantic import BaseModel

class data(BaseModel):
    assignment_no:int
    course_code:int
    course_title:str
    student_name:str
    registration_id:int
    questions:list[str]
    language:str