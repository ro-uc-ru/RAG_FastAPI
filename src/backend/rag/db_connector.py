import os
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv

load_dotenv()
#we need the path of our ChromaDB folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_DIR = os.path.join(BASE_DIR, '..', '..', 'chromadb')

def vector_store() -> Chroma:
    embedding = CohereEmbeddings(model = "embed-v4.0", cohere_api_key= os.getenv("COHERE-API-KEY")) # type: ignore
    return Chroma(
        collection_name= "PDFs",
        persist_directory = CHROMA_DB_DIR, 
        embedding_function = embedding)