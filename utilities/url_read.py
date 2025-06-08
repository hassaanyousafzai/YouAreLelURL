from langchain_community.document_loaders.url import UnstructuredURLLoader


def url_read(urls):
    if not urls:
        return ""
        
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    
    return documents

# if __name__ == "__main__":
#     url_read()
