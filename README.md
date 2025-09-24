
![Untitled Diagram](https://github.com/user-attachments/assets/64838eac-ec83-4672-9703-051f689b858f)

# 🩺 RAG Health Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers health-related queries using PMC (PubMed Central) articles.
The system uses FAISS for vector search, SentenceTransformers for embeddings, and a Qwen model from HuggingFace for response generation.

# 🚀 System Flow

**1. Data Preparation**

-> Download PMC articles (XML format)
  
-> Extract and split text into chunks
  
-> Generate embeddings with SentenceTransformers
  
-> Store embeddings in FAISS index

**2. Retrieval**

-> User asks a question via the Streamlit app

-> FAISS retrieves top relevant chunks

**3. Generation**

-> Retrieved context + user query sent to HuggingFace Qwen model

-> Model generates an answer

**4. Response**

-> Answer displayed in Streamlit interface

# 🛠 How to Operate

**1. Clone The Repository**

```
git clone https://github.com/jefanno1/rag_health_chatbot.git
cd rag_health_chatbot
```
**2. Create a virtual environment and install dependencies**
```
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
**3. Set HuggingFace API key**
```
# Windows
set HF_TOKEN=your_huggingface_token

# Mac/Linux
export HF_TOKEN=your_huggingface_token
```
**4. Prepare the FAISS index and corpus**

Run the indexing script (downloads articles, chunks them, and builds FAISS index):
```
python prepare_index.py
```
**5. Start the chatbot app**
```
streamlit run app.py
```
Then open the URL shown in your terminal (usually http://localhost:8501) to chat with the model.
