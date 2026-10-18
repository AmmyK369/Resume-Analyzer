
from fastapi import FastAPI, File, UploadFile , Form
import pdfplumber
from extract import extract_resume_data, extract_job_data  # for tekking groq what to extract
from schemas import ResumeData, AnalysisResult#for structure,shape of the text
from score import calculate_score

app=FastAPI()

def  read_pdf_text(upload: UploadFile)-> str:
    text= ""
    with pdfplumber.open(upload.file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text

@app.get("/")
def home():
    return{"message": "App is running"}

# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}


# @app.post("/extract/")
# async def create_upload_file(file: UploadFile):
#     all_text = ""     #an empty box to collect the text
#     with pdfplumber.open(file.file) as pdf:  
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             all_text += (page_text or "") + "\n" #add pages to the box and then new line
#     return {"text": all_text}


@app.post("/extract", response_model=ResumeData) # tells fastapi the shape of the endpoint(input) (connected schema here)
def extract_from_pdf(file: UploadFile): #endpoint fn is called dont mis it with extract.py
    return extract_resume_data(read_pdf_text)

@app.post("/analyze", response_model=AnalysisResult)
def analyze(file:UploadFile, job_description: str= Form(...)): #Form(...) tells FastAPI that job_description arrives as a form field alongside the file. A file upload and plain text can travel in the same request.
    resume = extract_resume_data(read_pdf_text(file))
    job= extract_job_data(job_description)
    return calculate_score(resume.skills,job.required_skills)
    