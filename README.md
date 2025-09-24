
![Untitled Diagram](https://github.com/user-attachments/assets/28f99efd-15cf-495e-b953-8e3ab33813ff)

---

# RAG Health Chatbot
This repository contains the code for a Retrieval-Augmented Generation (RAG) chatbot using PMC articles.  
The chatbot uses FAISS for vector search and a SentenceTransformer for embeddings, with LLM inference via HuggingFace Qwen model.

---

## ⚠️ Note

Some large/generated files are **not included** in this repository, because they can be recreated using the scripts:

- all_chunks.json
- corpus.json
- faiss_index.bin
- pmc_articles/ (downloaded PMC XML articles)

These files are ignored in `.gitignore`.

---

RAG Health Chatbot – System Flow

1. Data Preparation

- Download PMC articles (XML format)

- Extract text and split into chunks (prepare_index.py)

- Generate embeddings with SentenceTransformers

- Store embeddings in FAISS index

2. Retrieval

- User submits a query in Streamlit app (app.py)

- Retrieve top relevant chunks from FAISS

3. Generation

- Forward retrieved context + query to HuggingFace Qwen model (rag_api.py)

- Model generates an answer

4. Response

- Display answer back in the Streamlit interface
- The LLM requires HuggingFace Qwen access with your API key.

