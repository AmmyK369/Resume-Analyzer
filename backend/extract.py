import os
from dotenv import load_dotenv
from groq import Groq
from schemas import ResumeData, JobData

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

# The underscore in _ask_llm is 
# a Python convention meaning “internal helper, used only inside this file”.

def _ask_llm(system_prompt: str, user_text: str) ->str:
    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_text}
        ],
        response_format={"type":"json_object"},
    )
    return response.choices[0].message.content

def extract_resume_data(resume_text:str)-> ResumeData: 
    #takes string returns resumedata object
    # response=client.chat.completions.create( # resume text is the user msgs
    
    # code:
    #     model="openai/gpt-oss-120b",  
    #     messages=[
    #         {
    #             "role":"system",
    #             "content":"You extract data from resumes. Return only JSON with keys: skills (list of strings), education (string).",
                
    #         },
    #         {
    #             "role":"user",
    #             "content":resume_text
    #         },
    #     ],
    #     response_format={"type":"json_object"},
        
    # )
    # raw_json=response.choices[0].message.content
    
    raw_json= _ask_llm(
        "You extract data from resumes. Return only JSON with keys: skills (list of strings), education (string).",
        resume_text,
    )
    return ResumeData.model_validate_json(raw_json) #if valid returns resumedata object
                                                    # otherwise raises vlaidation error

def extract_job_data(job_text: str) ->JobData:
    raw_json = _ask_llm(
        "You extract required skills from job descriptions. Return only JSON with key: required_skills (list of strings).",
        job_text,
    )
    
    return JobData.model_validate_json(raw_json)
    
    