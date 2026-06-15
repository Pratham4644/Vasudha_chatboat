# import numpy as np
# from sentence_transformers import SentenceTransformer
# import streamlit as st


# @st.cache_resource
# def load_embed_model():
#     return SentenceTransformer("all-MiniLM-L6-v2")

# embed_model = load_embed_model()


# def search_index(index, metadata, query, top_k=3):
#     if index is None or not metadata:
#         return []

#     query_embedding = embed_model.encode(
#         [query],
#         normalize_embeddings=True
#     ).astype("float32")

#     distances, indices = index.search(query_embedding, top_k)

#     results = []
#     for idx in indices[0]:
#         if idx < len(metadata):
#             results.append(metadata[idx])

#     return results


# def retrieve_combined(
#     query,
#     main_index,
#     main_metadata,
#     temp_index=None,
#     temp_metadata=None,
#     top_k=3,
#     max_chars=3000
# ):
#     # Permanent KB search
#     main_results = search_index(
#         main_index,
#         main_metadata,
#         query,
#         top_k
#     )

#     # Uploaded file search
#     temp_results = search_index(
#         temp_index,
#         temp_metadata,
#         query,
#         top_k
#     )

#     # Merge results
#     combined_results = main_results + temp_results

#     # Combine text safely
#     context_text = "\n\n".join([r["text"] for r in combined_results])

#     # Extract clean source names only
#     sources = list(set([r.get("source_file", "Unknown") for r in combined_results]))

#     return context_text[:max_chars], sources













import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st


@st.cache_resource
def load_embed_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embed_model = load_embed_model()


def search_index(index, metadata, query, top_k=3):
    if index is None or not metadata:
        return []

    query_embedding = embed_model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):          # FIX: guard against -1 sentinel from FAISS
            results.append(metadata[idx])

    return results


def retrieve_combined(
    query,
    main_index,
    main_metadata,
    temp_index=None,
    temp_metadata=None,
    top_k=3,
    max_chars=6000          # ← increase this (was 3000)
):
    # Permanent KB search
    main_results = search_index(main_index, main_metadata, query, top_k)

    # Uploaded file search
    temp_results = search_index(temp_index, temp_metadata, query, top_k)

    # Merge results (temp docs take priority — listed first)
    combined_results = temp_results + main_results

    if not combined_results:
        # FIX: return a clear signal instead of empty string so the
        # generator knows there is no KB context and can say so honestly
        # rather than repeating the same generic fallback every time.
        return None, []

    # Deduplicate by text content to avoid repeated chunks
    seen = set()
    deduped = []
    for r in combined_results:
        txt = r.get("text", "").strip()
        if txt and txt not in seen:
            seen.add(txt)
            deduped.append(r)

    context_text = "\n\n".join([r["text"] for r in deduped])

    # Extract clean source names — handle both "source" (temp_index) and "source_file" (main_kb)
    sources = list(set([
        r.get("source") or r.get("source_file") or "Unknown"
        for r in deduped
    ]))

    return context_text[:max_chars], sources