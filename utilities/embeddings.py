from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

TF_ENABLE_ONEDNN_OPTS=0

def create_embeddings():
    # Create and return the embedding model
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def vector_store(chunks, embedding_model):
    vectors = FAISS.from_documents(chunks, embedding_model)
    return vectors





