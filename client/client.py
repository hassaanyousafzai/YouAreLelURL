from langchain_groq import ChatGroq

def llm_client():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.8,
        max_tokens=1024
    )
        
    return llm