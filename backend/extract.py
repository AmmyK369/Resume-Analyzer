import os
from dotenv import load_dotenv
from groq import Groq
from schemas import ResumeData

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
def extract_resume_data(resume_text:str)-> ResumeData: #takes string returns resumedata object
    response=client.chat.completions.create( # resume text is the user msgs
        model="openai/gpt-oss-120b",  
        messages=[
            {
                "role":"system",
                "content":"You extract data from resumes. Return only JSON with keys: skills (list of strings), education (string).",
                
            },
            {
                "role":"user",
                "content":resume_text
            },
        ],
        response_format={"type":"json_object"},
        
    )
    raw_json=response.choices[0].message.content
    return ResumeData.model_validate_json(raw_json) #if valid returns resumedata object
# otherwise raises vlaidation error