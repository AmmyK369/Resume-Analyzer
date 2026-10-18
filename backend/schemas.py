from pydantic import BaseModel

class ResumeData(BaseModel):
    skills:list[str]
    education:str
    
    # it tells the shape of the input