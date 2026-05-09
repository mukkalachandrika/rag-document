\# Project 3 — GenAI Document Q\&A Assistant (RAG)



A Flask web app where the user uploads a PDF and asks questions about it. The assistant answers strictly from the document content using a full RAG (Retrieval-Augmented Generation) pipeline including PDF parsing, embeddings, vector search, and LLM generation.



\---



\## Point 1 — Project Understanding



\### Problem Being Solved

Reading long PDF documents to find specific information is time consuming. This app lets the user upload any PDF and ask questions in plain English. The AI answers only from the document content — no hallucination, no outside knowledge.



\### User Actions Supported

\- Upload a PDF document (text-based, with tables and images described in text)

\- Ask any question about the document in natural language

\- Receive an answer grounded strictly in the document content

\- See the source excerpt from the document that the answer was based on

\- Use quick-prompt chips for common queries

\- Upload a new document at any time



\### Data Involved

\- Uploaded PDF file stored temporarily in the uploads folder

\- Extracted text stored in memory as chunks (not in a database)

\- Each chunk is approximately 500 words with 100-word overlap

\- Vector embeddings generated locally using sentence-transformers

\- FAISS index built in memory for similarity search

\- No user data is saved to disk permanently



\### Constraints and Guardrails

\- LLM is strictly instructed to answer ONLY from document content

\- LLM is told to say "I could not find this in the document" if answer is not present

\- This prevents hallucination and ensures answers are grounded

\- Only text-based PDFs are supported (scanned image-only PDFs will not work well)



\---



\## Point 2 — Tools and Technologies



\- Language: Python 3

\- Framework: Flask (web server and routing)

\- LLM Provider: Groq API (free tier)

\- LLM Model: llama-3.3-70b-versatile

\- Embeddings: sentence-transformers library, model all-MiniLM-L6-v2 (runs locally, free)

\- Vector Store: FAISS (runs locally, free, no cloud needed)

\- PDF Parsing: PyMuPDF (fitz) — extracts text page by page

\- Frontend: HTML, CSS (no frameworks)

\- Version Control: Git, GitHub



\---



\## Point 3 — Approach and Implementation



\### Step by Step How It Was Built



1\. Built PDF upload route in Flask — saves PDF to uploads folder

2\. Built rag.py to handle the full RAG pipeline

3\. Used PyMuPDF to extract text from every page of the PDF

4\. Split extracted text into overlapping chunks of 500 words with 100-word overlap so context is not lost at chunk boundaries

5\. Used sentence-transformers to convert each chunk into a vector embedding

6\. Stored all embeddings in a FAISS index in memory

7\. When user asks a question, the question is also converted to a vector embedding

8\. FAISS finds the top 5 most similar chunks to the question

9\. Those 5 chunks plus the question are sent to Groq LLaMA 3 as context

10\. LLM generates an answer using only those chunks

11\. Answer and source excerpt are shown in the chat UI



\### LLM Prompt Design



First iteration (LLM was answering from general knowledge, not document):

"Answer this question: {question}"



Second iteration (added context but LLM still sometimes used outside knowledge):

"Here is some text: {chunks}. Answer: {question}"



Final prompt (strict grounding, prevents hallucination):

\- Clearly tells the model it is a document assistant

\- Provides the retrieved chunks labeled as document content

\- Explicitly instructs: answer ONLY from the document content provided

\- Explicitly instructs: if the answer is not in the document, say so clearly

\- Forbids using any outside knowledge

\- Asks for a clear, concise answer



\### Key Architecture Decisions

\- FAISS was chosen over ChromaDB because it is lighter and needs zero setup

\- sentence-transformers runs completely locally so no embedding API cost

\- Overlapping chunks (100-word overlap) prevent losing context at boundaries

\- Everything is stored in memory per session — no database needed for RAG



\---



\## Point 4 — What Has Been Implemented



\### Working Features Delivered

\- PDF upload page with drag and drop style UI

\- Full RAG pipeline — PDF parsing, chunking, embedding, FAISS indexing, retrieval

\- Natural language question answering strictly from document

\- Source excerpt shown below every answer

\- Quick prompt chips for common queries

\- New document upload button to reset and upload a different PDF

\- Answers grounded in document only — hallucination prevented

\- Clean dark-themed chat interface



\### What Was Not Implemented

\- Support for scanned/image-only PDFs (would need OCR like Tesseract)

\- Multi-document support (one PDF at a time)

\- Saving chat history to database

\- User authentication



\---



\## RAG Pipeline Summary



1\. User uploads PDF

2\. PyMuPDF extracts text page by page

3\. Text split into 500-word chunks with 100-word overlap

4\. sentence-transformers encodes each chunk into a vector

5\. FAISS indexes all vectors in memory

6\. User asks a question

7\. Question is encoded into a vector

8\. FAISS retrieves top 5 most similar chunks

9\. Chunks plus question sent to Groq LLaMA 3

10\. LLM answers using ONLY document content

11\. Answer and source shown in chat UI



\---



\## Setup and Run



1\. Clone the repo

&#x20;  git clone https://github.com/mukkalachandrika/rag-document.git

&#x20;  cd rag-document



2\. Install dependencies

&#x20;  pip install -r requirements.txt



3\. Set your Groq API key — free at console.groq.com

&#x20;  Windows: set GROQ\_API\_KEY=your-key-here

&#x20;  Mac/Linux: export GROQ\_API\_KEY=your-key-here



4\. Run the app

&#x20;  python app.py



5\. Open browser at http://localhost:5000



\---



\## Project Structure



rag\_document\_qa/

├── app.py            — Flask routes

├── rag.py            — PDF parsing, chunking, embeddings, FAISS, Groq API

├── requirements.txt

├── README.md

└── templates/

&#x20;   ├── index.html    — PDF upload page

&#x20;   └── chat.html     — Q\&A chat interface



\---



\## Screenshots



outputs have been attached with the folder named screenshots

