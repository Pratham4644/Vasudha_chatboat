import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

from utils.file_loader import extract_text
from utils.chunker import chunk_text

@st.cache_resource
def load_embed_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embed_model = load_embed_model()

def build_temp_index(uploaded_files):
    all_chunks = []
    metadata = []

    for file in uploaded_files:
        text = extract_text(file)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append({
                "source": file.name,
                "chunk_id": i,
                "text": chunk
            })

    if not all_chunks:
        return None, []

    embeddings = embed_model.encode(
        all_chunks,
        normalize_embeddings=True
    ).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, metadata