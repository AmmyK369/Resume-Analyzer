from pydantic import BaseModel

class ResumeData(BaseModel):
    skills:list[str]
    education:str
    
    # it tells the shape of the input
    
class JobData(BaseModel):   #LLM return here for job description
    required_skills :list[str]
    
class AnalysisResult(BaseModel): #API will return this to user
    score: int
    matched :list[str]
    missing: list[str]
        
    