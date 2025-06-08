from langchain_groq import ChatGroq

def llm_client():
    llm = ChatGroq(
        model_name="gemma2-9b-it",
        temperature=0.5,
        max_tokens=1024
    )
        
    return llm