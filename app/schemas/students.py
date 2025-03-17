from typing import List, Optional
from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    student_id: str
    course_ids: Optional[List[int]] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    id: int
    name: Optional[str] = None
    student_id: Optional[str] = None

class StudentOut(StudentBase):
    id: int
    courses: List[dict]
    
    class Config:
        from_attributes = True