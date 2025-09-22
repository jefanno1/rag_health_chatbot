import os
import json
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# =========================
# 0. Setup OpenAI client untuk HF router
# =========================
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN")  # pastikan HF_TOKEN sudah ada di environment
)
if not client.api_key:
    raise ValueError("HF_TOKEN belum diset di environment!")

# =========================
# 1. Load FAISS index & chunks
# =========================
index = faiss.read_index("faiss_index.bin")
with open("all_chunks.json", "r", encoding="utf-8") as f:
    all_chunks = json.load(f)

# =========================
# 2. Load embedding model
# =========================
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# =========================
# 3. Retrieval
# =========================
def retrieve(query, top_k=3):
    query_vec = embed_model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    return [all_chunks[i] for i in I[0]]

# =========================
# 4. Preprocess context
# =========================
def clean_context(text):
    text = re.sub(r'\[\s*\d+(\s*[,–-]\s*\d+)*\s*\]', '', text)
    text = re.sub(r'\(\s*\d+(\s*[,–-]\s*\d+)*\s*\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# =========================
# 5. LLM via OpenAI SDK (HF Qwen)
# =========================
def ask_llm_api(prompt, max_tokens=3000):
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct:together",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return completion.choices[0].message.content

# =========================
# 6. RAG function
# =========================
def answer_question(query, top_k=3, max_context_tokens=5000):
    chunks = retrieve(query, top_k=top_k)
    context_text = clean_context(" ".join(chunks))[:max_context_tokens]
    prompt = f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"
    return ask_llm_api(prompt)

# =========================
# 7. Test
# =========================
if __name__ == "__main__":
    q = input("Enter your question: ")
    ans = answer_question(q)
    print("Answer:", ans)
