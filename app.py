from flask import Flask, render_template, request, jsonify, session
import os
from rag import process_pdf, answer_question

app = Flask(__name__)
app.secret_key = "rag_secret_key_2025"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf"]
    if file.filename == "" or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    result = process_pdf(filepath)
    if "error" in result:
        return jsonify(result), 500

    session["pdf_name"] = file.filename
    session["chunk_count"] = result["chunk_count"]

    return jsonify({
        "success": True,
        "filename": file.filename,
        "chunk_count": result["chunk_count"]
    })

@app.route("/chat")
def chat():
    pdf_name = session.get("pdf_name", None)
    if not pdf_name:
        return render_template("index.html", error="Please upload a PDF first.")
    return render_template("chat.html", pdf_name=pdf_name)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question"}), 400

    if not session.get("pdf_name"):
        return jsonify({"error": "No PDF loaded. Please upload a document first."}), 400

    result = answer_question(question)
    return jsonify(result)

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
