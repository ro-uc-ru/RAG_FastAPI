from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from backend.rag.tools import process_pdf
from backend.rag.agent import run_query_with_graph
import os
from logger import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', '..', 'uploaded')  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(
    title = "PDF RAG Assistant"
)
logger.info("Starting API")

@app.get('/')
async def root() -> dict[str, int]:
    return {"status": 200}

@app.post('/post-pdf')
async def upload_pdf(file: UploadFile) -> dict[str, str]:
    logger.info("Posting PDF")
    try:
        file_path = f"{UPLOAD_FOLDER}{file.filename}"
        with open(file_path, 'wb') as f:
            #we write the content to the folder so we can save it there
            content = await file.read()
            f.write(content)
            #we also process the file to ChromaDB
            process_pdf(path = file_path)

            #if succesfully uploaded, we let the user know it
            logger.info("PDF uploaded succesfully")
            return {
                "message": f"File {file.filename} uploaded succesfully in {UPLOAD_FOLDER} folder"
                }
        
    except Exception as e:
        logger.error("PDF not uploaded, error while uploading")
        return {
            "message": str(e)
            }


#we create a pydantic base model for handling queries about the pdf
class Query(BaseModel):
    query: str

@app.post('/query')
async def query_rag(query: Query):
    logger.info("Asking the agent about the PDF")
    response =  run_query_with_graph(query.query)
    return {
        "answer": response
    }
