import os, json, re, requests
from tqdm import tqdm
from Bio import Entrez
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# =========================
# 1. Search PMC
# =========================
Entrez.email = "youremail@example.com"
keyword = '"diabetes"[Title/Abstract] AND english[lang]'
retmax = 1000  # jumlah artikel

handle = Entrez.esearch(db="pmc", term=keyword, retmax=retmax)
record = Entrez.read(handle)
pmc_ids = record["IdList"]

print("Found PMC IDs:", pmc_ids)

# =========================
# 2. Download XML
# =========================
os.makedirs("pmc_articles", exist_ok=True)

for pmc_id in tqdm(pmc_ids, desc="Downloading PMC articles"):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:{pmc_id}&metadataPrefix=pmc"
    r = requests.get(url)
    with open(f"pmc_articles/{pmc_id}.xml", "wb") as f:
        f.write(r.content)

# =========================
# 3. Extract Text
# =========================
def extract_text_no_tables(xml_file):
    with open(xml_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse XML
    soup = BeautifulSoup(content, "lxml-xml")

    # Ambil judul
    title_tag = soup.find("article-title")
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    # Ambil abstrak
    abstract_tag = soup.find("abstract")
    abstract = abstract_tag.get_text(" ", strip=True) if abstract_tag else ""

    # Ambil body tanpa tabel, caption, atau footnote
    body_tag = soup.find("body")
    if body_tag:  # pastikan body ada
        for tag_name in ["table-wrap", "table", "fig", "fig-group", "caption"]:
            for t in body_tag.find_all(tag_name):
                t.decompose()  # hapus tag beserta isinya

        # Ambil teks setelah dihapus table/fig/caption
        body_text = []
        for p in body_tag.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                body_text.append(text)
    else:
        body_text = []



    body = " ".join(body_text)

    # Bersihkan teks: hapus referensi seperti [1], [2]
    text = f"{title}\n{abstract}\n{body}"
    text = re.sub(r"\(\s*\d+(\s*[–,-]\s*\d+)?(\s*,\s*\d+(\s*[–,-]\s*\d+)?)?\s*\)", "", text)
    # - [1], [1, 2], [ 1 , 2 , 3 ]
    text = re.sub(r"\[\s*\d+(\s*,\s*\d+)*\s*\]", "", text)
    text = re.sub(r"\[[0-9]+\]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# 4. Build corpus.json
# =========================
corpus = []
for pmc_id in tqdm(pmc_ids, desc="Extracting texts"):
    xml_file = f"pmc_articles/{pmc_id}.xml"
    text = extract_text_no_tables(xml_file)
    if len(text) > 50:  # skip kosong
        corpus.append({"id": pmc_id, "text": text})

with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Saved {len(corpus)} articles to corpus.json")

# =========================
# 5. Chunking
# =========================
def chunk_text(text, max_words=150, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words - overlap):
        chunks.append(" ".join(words[i:i+max_words]))
    return chunks

all_chunks = []
for article in corpus:
    chunks = chunk_text(article["text"])
    all_chunks.extend(chunks)

print(f"Total chunks: {len(all_chunks)}")

# =========================
# 6. Embeddings & FAISS index
# =========================
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(all_chunks, show_progress_bar=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))
faiss.write_index(index, "faiss_index.bin")  # simpan FAISS index
with open("all_chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print("FAISS index dan chunks tersimpan. Siap untuk RAG!")


# # =========================
# # Example query
# # =========================
# def search(query, k=3):
#     query_emb = model.encode([query])
#     D, I = index.search(np.array(query_emb), k)
#     return [all_chunks[i] for i in I[0]]

# query = "Apa gejala awal diabetes tipe 2?"
# results = search(query, k=5)
# print("Top 5 relevant chunks:")
# for r in results:
#     print("-", r[:200], "...")
