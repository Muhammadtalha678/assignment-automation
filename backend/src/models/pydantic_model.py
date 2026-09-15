from pydantic import BaseModel
from typing import Dict, List, Optional
class data(BaseModel):
    user_uuid:str #Frontend se aayi hui unique tab session ID
    assignment_no:int
    course_code:int
    semester:str
    student_name:str
    registration_id:str
    questions:list[str]
    language:str
    logo_path:Optional[str] = None #bd ma hm add krain gy path is liye optional none
    injected_cookies: List[Dict]
    
class Diagram(BaseModel):
    title: str
    diagram_type: str
    layout: str
    nodes: list[str]
    connections: list[list[str]]

class Section(BaseModel):
    heading:str
    explanation:str

class Question(BaseModel):
    question_number:int
    question_text:str
    introduction:str
    sections:list[Section]
    # diagram:Diagram
    diagram_prompt:str
    conclusion:str
    
class Assignment(BaseModel):
    assignment_no:int
    course_code:int
    semester:str
    student_name:str
    registration_id:str
    questions:list[Question]