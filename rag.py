import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq

# ── Models (loaded once) ──────────────────────────────────────────────────────
embedder = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Global vector store ───────────────────────────────────────────────────────
vector_index = None
stored_chunks = []


def extract_text_from_pdf(filepath: str) -> str:
    doc = fitz.open(filepath)
    full_text = ""
    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n[Page {page_num + 1}]\n{text}"
    doc.close()
    return full_text


def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def process_pdf(filepath: str) -> dict:
    global vector_index, stored_chunks
    try:
        text = extract_text_from_pdf(filepath)
        if not text.strip():
            return {"error": "Could not extract text from this PDF. It may be scanned/image-only."}

        chunks = split_into_chunks(text)
        stored_chunks = chunks

        embeddings = embedder.encode(chunks, show_progress_bar=False)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        vector_index = faiss.IndexFlatL2(dimension)
        vector_index.add(embeddings)

        return {"success": True, "chunk_count": len(chunks)}
    except Exception as e:
        return {"error": str(e)}


def retrieve_relevant_chunks(question: str, top_k: int = 5) -> list:
    question_embedding = embedder.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = vector_index.search(question_embedding, top_k)
    return [stored_chunks[i] for i in indices[0] if i < len(stored_chunks)]


def answer_question(question: str) -> dict:
    global vector_index
    if vector_index is None:
        return {"error": "No document loaded. Please upload a PDF first."}

    try:
        relevant_chunks = retrieve_relevant_chunks(question, top_k=5)
        context = "\n\n---\n\n".join(relevant_chunks)

        prompt = f"""You are a document assistant. Answer the user's question using ONLY the document content provided below.
If the answer is not found in the document, say: "I could not find this information in the uploaded document."
Do NOT use any outside knowledge.

DOCUMENT CONTENT:
{context}

USER QUESTION: {question}

Answer clearly and concisely based only on the document above:"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        return {
            "answer": answer,
            "sources": relevant_chunks[:2]
        }
    except Exception as e:
        return {"error": str(e)}
