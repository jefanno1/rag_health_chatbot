# 🩺 RAG Health Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers health-related queries using PMC (PubMed Central) articles.
The system uses FAISS for vector search, SentenceTransformers for embeddings, and a Qwen model from HuggingFace for response generation.

# 🚀 System Flow

1. Data Preparation

-> Download PMC articles (XML format)
  
-> Extract and split text into chunks
  
-> Generate embeddings with SentenceTransformers
  
-> Store embeddings in FAISS index

2. Retrieval

-> User asks a question via the Streamlit app

-> FAISS retrieves top relevant chunks

3. Generation

-> Retrieved context + user query sent to HuggingFace Qwen model

-> Model generates an answer

 4. Response

-> Answer displayed in Streamlit interface
