
from fastapi import FastAPI, File, UploadFile 
import pdfplumber
from extract import extract_resume_data  # for tekking groq what to extract
from schemas import ResumeData   #for structure,shape of the text

app=FastAPI()

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
    text = ""
    with pdfplumber.open(file.file) as pdf: # extracting text with pdf plumber
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return extract_resume_data(text) # the groq extracts info, validates with pydantic and return resumedata object