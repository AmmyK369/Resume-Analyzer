from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile 
import pdfplumber

app=FastAPI()

@app.get("/")
def home():
    return{"message": "App is running"}

# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}


@app.post("/extract/")
async def create_upload_file(file: UploadFile):
    all_text = ""     #an empty box to collect the text
    with pdfplumber.open(file.file) as pdf:  
        for page in pdf.pages:
            page_text = page.extract_text()
            all_text += (page_text or "") + "\n" #add pages to the box and then new line
    return {"text": all_text}

