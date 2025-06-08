import os
import pickle
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from client.client import llm_client
from langchain_groq import ChatGroq
from utilities.url_read import url_read
from utilities.recursive_chunks import recursive_chunks
from utilities.embeddings import create_embeddings, vector_store

from langchain.chains import RetrievalQAWithSourcesChain

def process_urls(urls, status_container):
    """Process multiple URLs and combine their data"""
    all_data = []
    
    # Filter out empty URLs
    valid_urls = [url for url in urls if url.strip()]
    
    if not valid_urls:
        raise ValueError("No valid URLs provided")
        
    for i, url in enumerate(valid_urls, 1):
        status_container.info(f"Processing URL {i} of {len(valid_urls)}...")
        url_data = url_read([url])  # Process single URL
        all_data.extend(url_data)  # Combine data
        
    return all_data

def show_chat_interface(file_path, llm):
    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    st.subheader("Chat History")
    if not st.session_state.messages:
        st.info("No messages yet. Start chatting!")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about the URLs..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        if os.path.exists(file_path):
            # Display assistant response with loading state
            with st.chat_message("assistant"):
                process_placeholder = st.empty()
                process_placeholder.text("Processing your query...")
                
                with open(file_path, "rb") as f:
                    vector_data = pickle.load(f)
                    
                    with st.spinner("Analyzing context and generating response..."):
                        process_placeholder.text("⏳ Processing...")
                    
                    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_data.as_retriever())
                    result = chain({"question": prompt}, return_only_outputs=True)
                    
                    # Clear the processing message and show the answer
                    process_placeholder.empty()
                    st.markdown(result["answer"])
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"]
                    })

def main():
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not found. Please create a .env file with your Groq API key: GROQ_API_KEY=your-api-key-here")
        return

    file_path = "vector_store.pkl"
    llm = llm_client()

    st.title("YouAreLeL (URL) Reader")
    st.text("A powerful tool that reads and analyzes content from multiple URLs, allowing you to chat and ask questions about the information contained within them. Perfect for research and content analysis.")
    st.text("Note: First-time processing may take a few moments as we set up the AI components.")

    # Sidebar inputs
    with st.sidebar:
        st.subheader("URL Configuration")
        url_inputs = [st.text_input(f"URL {i+1}", key=f"url_{i}") for i in range(3)]
        process_button = st.button("Process URLs", key="process_btn")
        
        # Add chat control buttons
        st.subheader("Chat Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("Export Chat"):
                chat_text = "\n\n".join([
                    f"{'Bot' if msg['role'] == 'assistant' else 'You'}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                st.download_button(
                    "Download Chat",
                    chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain"
                )

    # Main content area for status messages
    status_container = st.empty()

    if process_button:
        try:
            # Process all URLs and combine their data
            status_container.info("Processing URLs...")
            combined_data = process_urls(url_inputs, status_container)
            
            status_container.info("Creating text chunks...")
            chunks = recursive_chunks(combined_data)

            status_container.info("Creating embeddings...")
            embedding_model = create_embeddings()
            vector_store_data = vector_store(chunks, embedding_model)

            with open(file_path, "wb") as f:
                pickle.dump(vector_store_data, f)

            status_container.success(f"Successfully processed {len([url for url in url_inputs if url.strip()])} URLs! You can now start chatting.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Show chat interface
    if not os.path.exists(file_path):
        st.info("Please process some URLs first before we can chat about them!")
    else:
        show_chat_interface(file_path, llm)

if __name__ == "__main__":
    main()