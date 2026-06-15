import json
from pathlib import Path
import sys

import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_FILE = BASE_DIR / "data" / "index" / "faiss.index"
META_FILE = BASE_DIR / "data" / "index" / "metadata.json"

if not INDEX_FILE.exists():
    raise FileNotFoundError(f"Index file not found: {INDEX_FILE}")
if not META_FILE.exists():
    raise FileNotFoundError(f"Metadata file not found: {META_FILE}")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading index...")
index = faiss.read_index(str(INDEX_FILE))

print("Loading metadata...")
with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def search(query, top_k=3):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    ).astype("float32")
    _, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(metadata):
            results.append(metadata[i])

    return results


query = input("Enter your question: ").strip()
results = search(query)

print("\nTop Results:\n")
for i, r in enumerate(results, start=1):
    print(f"Result {i}")
    print("Crop:", r.get("crop", "unknown"))
    print("Text:", r.get("text", "")[:500])
    print("-" * 50)
