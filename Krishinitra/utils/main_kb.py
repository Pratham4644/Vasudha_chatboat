import faiss
import json
import os
from sentence_transformers import SentenceTransformer
import streamlit as st

# Get the path to the Krishinitra directory (parent of utils)
KRISHINITRA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_FILE = os.path.join(KRISHINITRA_DIR, "data", "index", "faiss.index")
META_FILE = os.path.join(KRISHINITRA_DIR, "data", "index", "metadata.json")

@st.cache_resource
def load_embed_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_main_index():
    try:
        if not os.path.exists(INDEX_FILE):
            st.error(f"FAISS index not found at: {INDEX_FILE}")
            return None
        return faiss.read_index(INDEX_FILE)
    except Exception as e:
        st.error(f"Could not load FAISS index: {e}")
        return None

@st.cache_resource
def load_main_metadata():
    try:
        if not os.path.exists(META_FILE):
            st.error(f"Metadata file not found at: {META_FILE}")
            return None
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Could not load metadata: {e}")
        return None


embed_model = load_embed_model
main_index = load_main_index
main_metadata = load_main_metadata