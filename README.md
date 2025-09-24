
![Untitled Diagram](https://github.com/user-attachments/assets/a8f8c08b-5d55-45e2-9130-4f4869abddb7)

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

## 🛠 Setup

1. Clone this repository

git clone https://github.com/jefanno1/rag_health_chatbot.git
cd rag_health_chatbot

2. Create and activate virtual environment
# Using venv
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

3. Set your HuggingFace API key
# On Windows
set HF_TOKEN=your_huggingface_token

# On Mac/Linux
export HF_TOKEN=your_huggingface_token

📂 Generate Data Files
python prepare_index.py

🖥 Run Chatbot
streamlit run app.py

📁 Folder Structure
Chatbot_Health_Project/
├─ pmc_articles/       # downloaded XML articles
├─ venv/               # virtual environment (ignored)
├─ __pycache__/        # Python cache (ignored)
├─ all_chunks.json     # chunks of articles (ignored)
├─ corpus.json         # full extracted corpus (ignored)
├─ faiss_index.bin     # FAISS index (ignored)
├─ app.py              # Streamlit interface
├─ rag_api.py          # RAG pipeline
├─ prepare_index.py    # script to generate corpus & FAISS index
├─ .gitignore          # ignore file

⚡ Notes

Make sure to run prepare_index.py before running app.py so the index and chunks exist.
The LLM requires HuggingFace Qwen access with your API key.

