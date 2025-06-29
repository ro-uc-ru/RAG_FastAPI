from .db_connector import vector_store
from .tools import process_pdf
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.retrieval_qa.base import BaseRetrievalQA, RetrievalQA
from .prompt import agent_prompt
from typing import TypedDict
from dotenv import load_dotenv
import os
load_dotenv()


class State(TypedDict):
    query: str
    answer: str
    docs: list


#to retrieve info about pdf
def __retrieve(state: State) -> State:
    chroma_db = vector_store()
    retriever = chroma_db.as_retriever()
    docs = retriever.invoke(state["query"], config=state.get("__run_config", {}))
    state["docs"] = docs 
    return state

#to generate responses about the pdf
def __generate(state: State) -> State:
    llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", google_api_key = os.getenv("GOOGLE-API-KEY"))
    qa: BaseRetrievalQA = RetrievalQA.from_llm(
        llm = llm,
        retriever = vector_store().as_retriever(),
        prompt = agent_prompt
    )
    answer = qa.run(state["query"])
    state["answer"] = answer 
    return state


#finally we create the graph
def __get_rag_graph():
    builder = StateGraph(State)
    
    builder.add_node("retrieve", __retrieve)
    builder.add_node("generate", __generate)

    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    graph = builder.compile()
    return graph



#we create a function to only return the answer
#this will be helpful while requesting querys using the API
def run_query_with_graph(query: str) -> str:
    graph = __get_rag_graph()
    result = graph.invoke({"query": query})
    return result["answer"]


