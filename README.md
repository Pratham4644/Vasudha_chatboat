# Vasudha — Offline Multimodal RAG for Agricultural Advisory

> **Fully offline. CPU-only. No cloud dependencies.**
> A retrieval-augmented generation system that lets farmers query agricultural knowledge using text — with multimodal (image + text) support actively in research.

---

## What This Is

Vasudha is an end-to-end offline RAG pipeline built for agricultural advisory in low-resource environments. It indexes domain-specific agronomic documents (crop guides, field manuals, disease references) and answers natural language queries entirely on-device — no internet, no GPU, no API calls.

The system was built from scratch as undergraduate research at ADCET, Sangli. It achieved **91% top-3 retrieval accuracy** on an internal pilot benchmark of 20 query-answer pairs, won **1st place at the ADCET internal hackathon**, and was selected to represent the college at the **DIPEX state-level project exhibition**.

It now forms the baseline for ongoing MEXT-funded research into **multimodal retrieval** — extending the pipeline to accept visual crop observations (photographs of disease symptoms) as queries alongside text.

---

## The Problem It Solves

Standard RAG systems are text-in, text-out. In agricultural advisory, that's a real constraint: a farmer observing an unfamiliar pattern of discolouration on a rice leaf cannot reliably translate that observation into a text query that recovers the correct document chunk. The visual symptom is the primary datum; its text description is a lossy approximation.

Vasudha's current version handles text queries efficiently and offline. The research extension addresses the modality mismatch — aligning visual crop features to the same embedding space as text, enabling joint visual-text retrieval over the same FAISS index.

---

## Pipeline Architecture

```
PDF Documents
      │
      ▼
 Text Extraction          ← PyMuPDF (fitz) | header/footer removal | normalization
      │
      ▼
   Chunking               ← Sentence-boundary overlap | heading-based splitting
      │
      ▼
  Embedding               ← all-MiniLM-L6-v2 (SentenceTransformers) | 384-dim
      │
      ▼
  FAISS Index             ← IndexFlatL2 | cosine similarity search
      │
      ▼
  Top-k Retrieval         ← Semantic search over knowledge base
      │
      ▼
Answer Generation         ← TinyLlama-1.1B via Ollama | streamed output
      │
      ▼
  Streamlit UI            ← Text query | voice input | uploaded document support
```

---

## Key Design Decisions

| Decision | Choice | Reason |
|---|---|---|
| Embedding model | `all-MiniLM-L6-v2` | 384-dim, competitive semantic similarity, runs on CPU |
| Vector index | FAISS `IndexFlatL2` | Keyword overlap (BM25) is poor proxy for domain-specific agronomic text |
| Generation model | TinyLlama-1.1B via Ollama | Smallest instruction-tuned LLaMA-family model producing coherent responses within 4 GB RAM |
| Retrieval metric | Top-3 accuracy | Practical threshold — user can scan 3 results in an advisory context |

---

## Results

| Metric | Value | Note |
|---|---|---|
| Top-3 Retrieval Accuracy | **91%** | Internal pilot, 20 manually constructed query-answer pairs |
| Hardware | CPU-only | Intel i5-8250U, 8 GB RAM — no GPU required |
| External APIs | None | Fully offline after model download |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| UI | Streamlit + streamlit-mic-recorder |
| PDF Processing | PyMuPDF (`fitz`) |
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Vector Search | FAISS (`faiss-cpu`) |
| LLM | TinyLlama-1.1B via Ollama |
| HTTP | Requests |
| Utilities | NumPy, tqdm |

---

## Project Structure

```
Krishinitra/
├── data/
│   ├── raw_pdfs/          # Source agronomic documents (wheat, cotton, sugarcane)
│   ├── extracted_text/    # Cleaned text output from PDFs
│   ├── chunks/            # Chunked JSON ready for embedding
│   └── index/             # FAISS index + metadata
├── scripts/
│   ├── extract_text.py    # PDF → cleaned text
│   ├── chunk_data.py      # Text → semantic chunks
│   ├── build_index.py     # Chunks → FAISS index
│   ├── rag_chat.py        # CLI RAG query interface
│   └── test_retrieval.py  # Index retrieval sanity check
├── ui/
│   └── app.py             # Streamlit front-end
└── utils/
    ├── file_loader.py     # Document loading
    ├── chunker.py         # Chunk splitting and preprocessing
    ├── main_kb.py         # Main knowledge base index loader
    ├── temp_index.py      # Temporary index for uploaded files
    ├── retriever.py       # Semantic search + result merging
    ├── generator.py       # Ollama streaming response handler
    ├── language_detector.py
    ├── speech_to_text.py
    └── translator.py
```

---

## Getting Started

**1. Install dependencies**
```bash
pip install streamlit faiss-cpu numpy sentence-transformers requests PyMuPDF tqdm streamlit-mic-recorder python-docx
```

**2. Add source PDFs**
```
Krishinitra/data/raw_pdfs/
```

**3. Run the pipeline**
```bash
python Krishinitra/scripts/extract_text.py
python Krishinitra/scripts/chunk_data.py
python Krishinitra/scripts/build_index.py
```

**4. Start Ollama and pull TinyLlama**
```bash
ollama serve
ollama pull tinyllama
```

**5. Launch the app**
```bash
streamlit run Krishinitra/ui/app.py
```

**6. CLI testing**
```bash
python Krishinitra/scripts/rag_chat.py
```

---

## Current Knowledge Base

Covers three crops currently indexed:

- **Wheat** — disease references, growth guides
- **Cotton** — pest and disease data
- **Sugarcane** — field manuals and advisory content

80+ documents targeted for the research extension phase.

---

## Research Extension (In Progress)

This project is the baseline system for ongoing research into **Multimodal RAG for Agricultural Advisory** — the proposed contribution for a MEXT 2027 research scholarship targeting the University of Tokyo, Tohoku University, and Osaka University.

The extension adds a **visual query path**: a lightweight vision encoder (<25M parameters) trained on PlantVillage crop disease data, aligned to the same 384-dimensional embedding space as the text encoder via contrastive projection. Both paths query the same FAISS index.

**Research objectives:**
- Benchmark MobileViT-XS, EfficientNet-B0, and ResNet-18 on CPU inference speed vs. classification accuracy
- Compare three alignment strategies: contrastive projection (CLIP-inspired), adapter fine-tuning, zero-shot linear projection
- Build and release a 200-query annotated multimodal benchmark for agricultural retrieval evaluation
- Profile end-to-end latency and memory on a 4 GB RAM CPU-only testbed

**Target conferences:** ACL Findings, EMNLP, IJCAI

---

## Running the Project (Step-by-Step)

All commands are run from the **root of the repository** (`Vasudha_chatboat/`).

### Step 1 — Clone the repo
```bash
git clone https://github.com/Pratham4644/Vasudha_chatboat.git
cd Vasudha_chatboat
```

### Step 2 — Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install streamlit faiss-cpu numpy sentence-transformers requests PyMuPDF tqdm streamlit-mic-recorder python-docx
```

### Step 4 — Install and start Ollama
Download Ollama from https://ollama.com and then run:
```bash
ollama serve
ollama pull tinyllama
```
Keep this running in a separate terminal.

### Step 5 — Build the knowledge base (one-time setup)
```bash
# Extract text from PDFs
python Krishinitra/scripts/extract_text.py

# Chunk the extracted text
python Krishinitra/scripts/chunk_data.py

# Build the FAISS index
python Krishinitra/scripts/build_index.py
```
This populates `Krishinitra/data/extracted_text/`, `Krishinitra/data/chunks/`, and `Krishinitra/data/index/`.

### Step 6 — Launch the Streamlit app
```bash
streamlit run Krishinitra/ui/app.py
```
Open your browser at `http://localhost:8501`

### Optional — CLI query interface
```bash
python Krishinitra/scripts/rag_chat.py
```

### Optional — Test retrieval sanity
```bash
python Krishinitra/scripts/test_retrieval.py
```

---

## About

Built by **Prathamesh Shinde**, B.Tech CSE, Annasaheb Dange College of Engineering and Technology (ADCET), Sangli, Maharashtra.

- Email: prathamps8666@gmail.com
- GitHub: [github.com/Pratham4644](https://github.com/Pratham4644)

---

*Vasudha means "the earth that sustains" — a fitting name for a system built to support the farmers who work it.*
