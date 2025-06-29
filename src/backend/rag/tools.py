from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .db_connector import vector_store
from langchain.schema import Document


#function to process and send PDF to ChromaDB
def process_pdf(path: str) -> None:
    #load the before saved and uploaded PDF
    loader = PyPDFLoader(path)
    doc: list[Document] = loader.load()

    #splitting PDF info so later we send it to ChromaDB
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    info = splitter.split_documents(doc)

    chroma_db = vector_store()
    chroma_db.add_documents(info)
    
    return None



