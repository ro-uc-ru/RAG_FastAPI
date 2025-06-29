from langchain_core.prompts import PromptTemplate

agent_prompt = PromptTemplate(
    input_variables = ['context', 'question'],
    template = """
        You are a helpful AI Agent that only answers questions about the following pieces of context.
        If you can't find the answer, do not hesitate to say you don't know the answer, but also don't try to make up an answer.
        Pay attention to the context of the question rather than only trying to find similar keywords on the corpus of the question.
        {context}
        Question: {question}
        Answer:

"""
)