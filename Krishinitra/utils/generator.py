import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

def stream_answer(context_text: str, question: str):

    full_prompt = f"""
You are an agricultural expert.

Answer ONLY from the given context.
Give a complete, detailed, step-by-step answer.
Do NOT cut the answer early.

If information is missing, reply exactly:
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
            "num_predict": 600,        # increased output length
            "temperature": 0.2,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=600   # increased timeout
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))
            except:
                continue

            if "response" in data:
                yield data["response"]

            if data.get("done", False):
                break

    except requests.exceptions.RequestException as e:
        yield f"\n[ERROR] Model connection failed: {str(e)}"



# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "tinyllama"


# def stream_answer(context_text: str | None, question: str):
#     """
#     Stream an answer from TinyLlama via Ollama.

#     If context_text is None (no KB chunks found), the LLM answers from
#     its own knowledge and tells the user no documents were matched.
#     """

#     if context_text:
#         prompt = f"""You are Krishinitra, an expert AI farming assistant.
# Use the context below to answer the farmer's question accurately and concisely.
# If the context does not fully cover the question, supplement with your own knowledge.

# Context:
# {context_text}

# Question: {question}

# Answer:"""
#     else:
#         # FIX: no context — ask the LLM to answer from general knowledge
#         # instead of silently using a hardcoded fallback every time.
#         prompt = f"""You are Krishinitra, an expert AI farming assistant.
# No specific documents were found for this query, so answer from your general
# agricultural knowledge. Be concise and practical.

# Question: {question}

# Answer:"""

#     payload = {
#         "model": MODEL_NAME,
#         "prompt": prompt,
#         "stream": True,
#     }

#     try:
#         with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60) as resp:
#             resp.raise_for_status()
#             for line in resp.iter_lines():
#                 if not line:
#                     continue
#                 import json
#                 chunk = json.loads(line)
#                 token = chunk.get("response", "")
#                 if token:
#                     yield token
#                 if chunk.get("done"):
#                     break

#     except requests.exceptions.ConnectionError:
#         yield (
#             "⚠️ Could not connect to Ollama. "
#             "Please make sure Ollama is running (`ollama serve`) and try again."
#         )
#     except requests.exceptions.Timeout:
#         yield "⚠️ The request timed out. The model may be loading — please try again."
#     except Exception as e:
#         yield f"⚠️ Unexpected error: {e}"