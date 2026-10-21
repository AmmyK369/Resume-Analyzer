
from fastapi import FastAPI, File, UploadFile , Form, HTTPException
import pdfplumber
from extract import extract_resume_data, extract_job_data  # for tekking groq what to extract
from schemas import ResumeData, AnalysisResult#for structure,shape of the text
from score import calculate_score
from pydantic import ValidationError

app=FastAPI()

def  read_pdf_text(upload: UploadFile)-> str:
    if not(upload.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a pdf file")
    text= ""
    try:
        with pdfplumber.open(upload.file) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read this pdf")
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text found in the pdf.Scanned or image-only PDFs are not supported.",
        )
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
    text = read_pdf_text(file)
    return extract_resume_data(text)

@app.post("/analyze", response_model=AnalysisResult)
def analyze(file:UploadFile, job_description: str= Form(...)): #Form(...) tells FastAPI that job_description arrives as a form field alongside the file. A file upload and plain text can travel in the same request.
    if not job_description.strip() or "":
        raise HTTPException(
            status_code=400,
            detail="Job description is empty"
        )
    try:
        resume = extract_resume_data(read_pdf_text(file))
        job= extract_job_data(job_description)
    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an unexpected format. Please try again.",
        )
    return calculate_score(resume.skills,job.required_skills)
    