import time
import faiss
import json
import requests
from sentence_transformers import SentenceTransformer

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

INDEX_FILE = "data/index/faiss.index"
META_FILE = "data/index/metadata.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

# ─────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────

print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(INDEX_FILE)

print("Loading metadata...")
with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# ─────────────────────────────────────────────
# RETRIEVAL
# ─────────────────────────────────────────────
def retrieve_context(query, top_k=3):
    t0 = time.perf_counter()

    query_embedding = embed_model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    t1 = time.perf_counter()

    distances, indices = index.search(query_embedding, top_k)

    t2 = time.perf_counter()

    combined = "\n\n".join(metadata[i]["text"] for i in indices[0])
    context = combined[:3500]

    print(f"[TIME] Embedding: {(t1 - t0)*1000:.1f} ms")
    print(f"[TIME] FAISS search: {(t2 - t1)*1000:.1f} ms")

    return context
# ─────────────────────────────────────────────
# GENERATION
# ─────────────────────────────────────────────

def generate_answer(context_text: str, question: str) -> str:
    full_prompt = f"""
You are an agricultural assistant.
Answer strictly using the context.
If missing, say:
Information not available in the knowledge base.

Context:
{context_text}

Question:
{question}

Answer:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": True,
        "options": {
            "num_predict": 4000,
            "temperature": 0.2,
            "stop": ["\n\nQuestion:", "\nContext:"]
        }
    }

    t0 = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=500
    )

    response.raise_for_status()

    first_token_time = None
    answer = ""

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line.decode("utf-8"))

        if "response" in data:
            if first_token_time is None:
                first_token_time = time.perf_counter()
                print(f"[TIME] First token: {(first_token_time - t0):.2f} sec")

            answer += data["response"]

        if data.get("done", False):
            break

    t_end = time.perf_counter()
    print(f"[TIME] Total generation: {(t_end - t0):.2f} sec")

    return answer.strip()

# ─────────────────────────────────────────────
# CHAT LOOP
# ─────────────────────────────────────────────

while True:
    question = input("\nAsk a farming question (type exit to quit): ").strip()

    if question.lower() == "exit":
        break

    context = retrieve_context(question)
    answer = generate_answer(context, question)

    print("\nAnswer:\n")
    print(answer)