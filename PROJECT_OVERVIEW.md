# Vasudha Chatboat Project Overview

## 📌 Project Description

Vasudha Chatboat is a Python-based retrieval-augmented generation (RAG) system for agricultural knowledge. The repository is organized under the name `Krishinitra` and currently focuses on the pipeline for extracting agricultural text from PDFs, chunking that text, building a FAISS similarity index, and generating answers via a locally served TinyLlama model.

The system includes:
- PDF extraction and cleaning
- Document chunking and filtering
- Embedding generation with SentenceTransformers
- FAISS vector indexing and semantic search
- Answer generation through Ollama / TinyLlama
- A Streamlit user interface for query interaction

---

## 🛠️ Technology Stack

- **Programming Language:** Python 3.x
- **UI / Front End:** Streamlit
- **Vector Search:** FAISS (`faiss-cpu` for CPU e   nvironments)
- **Embedding Model:** SentenceTransformers (`all-MiniLM-L6-v2`)
- **LLM Serving:** TinyLLaMA via Ollama
- **PDF/Text Processing:** PyMuPDF (`fitz`)
- **Document Formats:** PDF source files, extracted text saved as `.txt`
- **HTTP Client:** Requests
- **Utilities:** NumPy, tqdm, JSON, os, pathlib, regex

> ⚙️ The repository appears to be developed on Windows, but the Python code is generally portable across platforms.

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | UI framework for the front-end app |
| `faiss-cpu` | FAISS similarity search index |
| `sentence-transformers` | Text embedding generation |
| `numpy` | Numerical arrays and tensor support |
| `requests` | HTTP calls to Ollama / local model service |
| `PyMuPDF` (`fitz`) | PDF text extraction |
| `python-docx` | DOCX / text document support (utility imports) |
| `tqdm` | Progress bars during batch processing |
| `streamlit-mic-recorder` | Voice recording integration for UI |

> Note: `Krishinitra/requirements.txt/` is currently an empty directory placeholder and does not contain package listings.

---

## 🤖 Models & Project Modules

### External Models

- **SentenceTransformers** (`all-MiniLM-L6-v2`) for embedding chunks and queries.
- **TinyLLaMA** served locally via Ollama at `http://localhost:11434/api/generate`.

### Main Utility Modules (`Krishinitra/utils`)

| Module | Responsibility |
|---|---|
| `file_loader.py` | Extracts and loads text from documents |
| `chunker.py` | Chunk splitting and text preprocessing |
| `temp_index.py` | Builds a temporary FAISS index for uploaded files |
| `main_kb.py` | Loads the main knowledge-base FAISS index and metadata |
| `retriever.py` | Performs semantic search and combines results |
| `generator.py` | Streams answer tokens from the Ollama model |
| `language_detector.py` | Language detection utilities |
| `speech_to_text.py` | Speech transcription helpers |
| `translator.py` | Translation utilities |

### Pipeline Scripts (`Krishinitra/scripts`)

- `extract_text.py` — extracts and cleans text from PDFs in `Krishinitra/data/raw_pdfs`
- `chunk_data.py` — filters, splits, and saves semantic chunks to `Krishinitra/data/chunks/chunks.json`
- `build_index.py` — encodes chunks, builds the FAISS index, and writes metadata
- `rag_chat.py` — example RAG workflow to query the index and call Ollama
- `test_retrieval.py` — index retrieval sanity check

---

## 🗂️ Project Structure

```
├── Krishinitra/
│   ├── app/                      # placeholder directory
│   ├── data/                     # project data and cache directories
│   │   ├── chunks/               # chunk JSON output
│   │   ├── embeddings/           # embedding outputs / placeholders
│   │   ├── extracted_text/       # cleaned text files from PDFs
│   │   └── index/                # FAISS index + metadata
│   ├── main.py/                  # empty placeholder directory
│   ├── requirements.txt/        # empty placeholder directory
│   ├── scripts/                  # preprocessing and RAG scripts
│   │   ├── build_index.py
│   │   ├── chunk_data.py
│   │   ├── extract_text.py
│   │   ├── rag_chat.py
│   │   └── test_retrieval.py
│   ├── ui/                       # Streamlit front-end app
│   │   └── app.py
│   └── utils/                    # shared helper modules
│       ├── chunker.py
│       ├── file_loader.py
│       ├── generator.py
│       ├── language_detector.py
│       ├── main_kb.py
│       ├── retriever.py
│       ├── speech_to_text.py
│       ├── temp_index.py
│       ├── translator.py
│       └── __init__.py
├── data/                        # additional workspace data cache directories
│   ├── chunks/
│   ├── extracted_text/
│   └── index/
├── __init__.py
└── PROJECT_OVERVIEW.md
```

> The repository currently contains a few placeholder directories instead of real module files: `Krishinitra/main.py/` and `Krishinitra/requirements.txt/`.

---

## 🚀 Recommended Workflow

1. Install packages:

```bash
pip install streamlit faiss-cpu numpy sentence-transformers requests python-docx PyMuPDF tqdm streamlit-mic-recorder
```

2. Add source PDF files to `Krishinitra/data/raw_pdfs`.
3. Run extraction:

```bash
python Krishinitra/scripts/extract_text.py
```

4. Run chunking:

```bash
python Krishinitra/scripts/chunk_data.py
```

5. Build the FAISS index:

```bash
python Krishinitra/scripts/build_index.py
```

6. Start the Ollama service:

```bash
ollama serve
```

7. Launch the Streamlit app:

```bash
streamlit run Krishinitra/ui/app.py
```

8. For CLI testing:

```bash
python Krishinitra/scripts/rag_chat.py
```

---

## 🔧 Current Notes

- `Krishinitra/utils/main_kb.py` loads the main `faiss.index` and `metadata.json` from `Krishinitra/data/index`.
- `Krishinitra/utils/retriever.py` merges temporary upload results with the main knowledge base and returns combined context.
- `Krishinitra/utils/generator.py` streams generated text from Ollama using `tinyllama`.
- `Krishinitra/scripts/extract_text.py` performs PDF cleaning, header/footer removal, and text normalization.
- `Krishinitra/scripts/chunk_data.py` uses crop detection and heading-based splitting to keep farmer-focused content.

---

*Last updated: June 8, 2026.*
