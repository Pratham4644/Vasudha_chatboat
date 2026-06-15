import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


# CONFIG


CHUNKS_FILE = "data/chunks/chunks.json"
OUTPUT_DIR  = "data/index"
INDEX_FILE  = os.path.join(OUTPUT_DIR, "faiss.index")
META_FILE   = os.path.join(OUTPUT_DIR, "metadata.json")

MODEL_NAME = "all-MiniLM-L6-v2"


# INIT


os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)


# LOAD CHUNKS


with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

texts = [c["text"] for c in chunks]

# CREATE EMBEDDINGS


embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")

print("Embeddings shape:", embeddings.shape)


# BUILD FAISS INDEX


dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)   # Inner Product = cosine when normalized
index.add(embeddings)

print("FAISS index built")

# SAVE


faiss.write_index(index, INDEX_FILE)

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Saved:")
print(" -", INDEX_FILE)
print(" -", META_FILE)