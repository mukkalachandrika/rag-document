# Project 3 — GenAI Document Q&A Assistant (RAG)

A Flask web app where users upload a PDF and ask questions about it. Answers are generated using a full RAG (Retrieval-Augmented Generation) pipeline and come strictly from the document content.

## Tech Stack
- Backend: Python, Flask
- LLM: Groq API (llama-3.3-70b-versatile) — Free
- Embeddings: sentence-transformers (all-MiniLM-L6-v2) — Local, Free
- Vector Store: FAISS — Local, Free
- PDF Parsing: PyMuPDF (fitz)
- Frontend: HTML, CSS

## Setup and Run

1. Clone the repo
   git clone https://github.com/YOUR-USERNAME/rag-document-qa.git
   cd rag-document-qa

2. Install dependencies
   pip install -r requirements.txt

3. Set your Groq API key (free at console.groq.com)
   set GROQ_API_KEY=your-groq-key-here   (Windows)
   export GROQ_API_KEY=your-groq-key-here (Mac/Linux)

4. Run the app
   python app.py

5. Open browser
   http://localhost:5000

## RAG Pipeline (Step by Step)

1. User uploads a PDF
2. PyMuPDF extracts all text page by page
3. Text is split into 500-word overlapping chunks (100-word overlap)
4. sentence-transformers encodes each chunk into a vector embedding
5. FAISS indexes all embeddings in memory
6. User asks a question
7. Question is encoded into a vector
8. FAISS retrieves top 5 most similar chunks
9. Retrieved chunks + question are sent to Groq LLaMA 3
10. LLM answers using ONLY the document content
11. Answer + source excerpt shown in the chat UI

## Features
- Upload any text-based PDF
- Ask questions in natural language
- Answers strictly grounded in document content only
- Source excerpt shown with every answer
- Quick-prompt chips for common queries
- Upload a new document anytime with the + New Document button

## Project Structure

rag_document_qa/
├── app.py                  # Flask routes
├── rag.py                  # PDF processing, embeddings, FAISS, Groq
├── requirements.txt
├── README.md
└── templates/
    ├── index.html          # Upload page
    └── chat.html           # Q&A chat interface

## LLM Prompt Design

The prompt in rag.py:
- Instructs the model to answer ONLY from the provided document content
- Explicitly tells the model to say it could not find the answer if it is not in the document
- Prevents hallucination by forbidding outside knowledge
- Injects the top 5 retrieved chunks as context
- Asks for a clear and concise answer

## Screenshots

### Upload Page
![Upload Page](screenshots/upload.png)

### Chat Interface
![Chat Interface](screenshots/chat.png)

### Answer with Source
![Answer with Source](screenshots/answer.png)
