from langchain_text_splitters import RecursiveCharacterTextSplitter

def recursive_chunks(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(data)

    return chunks