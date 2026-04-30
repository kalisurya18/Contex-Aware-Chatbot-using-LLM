import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import uuid
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from config import Config
from utils.db import (
    init_db, create_conversation, get_conversations,
    delete_conversation, add_message, get_messages,
    add_feedback, save_document, get_documents,
)
from utils.Ollama_client import OllamaClient
from utils.rag import RAGEngine

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

ollama = OllamaClient()
rag = RAGEngine()

init_db()
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# ── Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    connected = ollama.check_connection()
    models = ollama.list_models() if connected else []
    return jsonify({
        "ollama_connected": connected,
        "current_model": Config.OLLAMA_MODEL,
        "available_models": models,
    })


@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    return jsonify(get_conversations())


@app.route("/api/conversations", methods=["POST"])
def new_conversation():
    data = request.json or {}
    conv_id = str(uuid.uuid4())
    title = data.get("title", "New Chat")
    category = data.get("category", "general")
    create_conversation(conv_id, title, category)
    return jsonify({"id": conv_id, "title": title, "category": category})


@app.route("/api/conversations/<conv_id>", methods=["DELETE"])
def remove_conversation(conv_id):
    delete_conversation(conv_id)
    return jsonify({"success": True})


@app.route("/api/conversations/<conv_id>/messages", methods=["GET"])
def list_messages(conv_id):
    return jsonify(get_messages(conv_id))


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    conversation_id = data.get("conversation_id")
    user_message = data.get("message", "").strip()
    category = data.get("category", None)

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        title = user_message[:50] + ("..." if len(user_message) > 50 else "")
        create_conversation(conversation_id, title, category or "general")

    add_message(conversation_id, "user", user_message)

    history = get_messages(conversation_id)
    messages = [{"role": m["role"], "content": m["content"]} for m in history]

    # context = rag.search(user_message, n_results=3, category=category)
    context = rag.search(user_message)

    result = ollama.generate_response(messages, context=context)

    if result["success"]:
        msg_id = add_message(conversation_id, "assistant", result["response"])
        return jsonify({
            "conversation_id": conversation_id,
            "message_id": msg_id,
            "response": result["response"],
            "model": result.get("model", ""),
            "context_used": bool(context),
        })
    else:
        return jsonify({
            "conversation_id": conversation_id,
            "response": result["response"],
            "error": True,
        })


@app.route("/api/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": f"File type not allowed. Supported: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        }), 400

    category = request.form.get("category", "general")
    original_name = file.filename
    filename = secure_filename(f"{uuid.uuid4()}_{original_name}")
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    chunk_count = rag.add_document(filepath, original_name, category)
    save_document(filename, original_name, category, chunk_count)

    return jsonify({
        "success": True,
        "filename": original_name,
        "chunks": chunk_count,
        "message": f"Document '{original_name}' processed into {chunk_count} chunks and indexed.",
    })


@app.route("/api/documents", methods=["GET"])
def list_documents():
    return jsonify(get_documents())


@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.json
    add_feedback(data.get("message_id"), data.get("rating"), data.get("comment", ""))
    return jsonify({"success": True})


@app.route("/api/suggestions")
def suggestions():
    category = request.args.get("category", "general")
    all_suggestions = {
        "general": [
            "What programs does the institution offer?",
            "Tell me about campus facilities",
            "What are the hostel options available?",
            "How can I contact the administration?",
        ],
        "academics": [
            "What are the CSE specializations?",
            "Explain the grading system",
            "What is the minimum attendance requirement?",
            "How many backlogs are allowed for promotion?",
        ],
        "admissions": [
            "What is the B.Tech admission process?",
            "What are the eligibility criteria for M.Tech?",
            "Tell me about the fee structure",
            "When do admissions start?",
        ],
        "placements": [
            "What is the placement percentage?",
            "Which are the top recruiting companies?",
            "What is the highest package offered?",
            "Tell me about the internship policy",
        ],
        "library": [
            "What are the library timings?",
            "How many books can I borrow?",
            "What e-resources are available?",
            "What is the late return fine?",
        ],
        "scholarships": [
            "What scholarships are available?",
            "How to apply for merit scholarship?",
            "Tell me about need-based financial aid",
            "What is the research fellowship amount?",
        ],
    }
    return jsonify(all_suggestions.get(category, all_suggestions["general"]))


# ── WebSocket for streaming ─────────────────────────────────────────────

@socketio.on("chat_stream")
def handle_stream(data):
    try:
        conversation_id = data.get("conversation_id")
        user_message = data.get("message", "").strip()
        category = data.get("category", None)

        if not user_message:
            emit("stream_error", {"error": "Empty message"})
            return

        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            title = user_message[:50] + ("..." if len(user_message) > 50 else "")
            create_conversation(conversation_id, title, category or "general")
            emit("conversation_created", {"id": conversation_id, "title": title})

        add_message(conversation_id, "user", user_message)

        history = get_messages(conversation_id)
        messages = [{"role": m["role"], "content": m["content"]} for m in history]
        # context = rag.search(user_message, n_results=3, category=category)
        context = rag.search(user_message)

        full_response = ""
        emit("stream_start", {"conversation_id": conversation_id})

        for token in ollama.stream_response(messages, context=context):
            if token.startswith("Error:"):
                emit("stream_error", {"error": token})
                break
            full_response += token
            emit("stream_token", {"token": token})

        if full_response and not full_response.startswith("Error:"):
            msg_id = add_message(conversation_id, "assistant", full_response)
            emit("stream_end", {
                "conversation_id": conversation_id,
                "message_id": msg_id,
                "context_used": bool(context),
            })
        elif not full_response:
            emit("stream_error", {"error": "No response received from model"})
    except Exception as e:
        emit("stream_error", {"error": f"Unexpected error: {str(e)}"})


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  EduBot - Context-Aware Educational Chatbot")
    print("=" * 60)
    print(f"  Ollama URL : {Config.OLLAMA_BASE_URL}")
    print(f"  Model      : {Config.OLLAMA_MODEL}")
    print(f"  Status     : {'Connected' if ollama.check_connection() else 'Not Connected'}")
    print("=" * 60)
    print("  Open http://localhost:5001 in your browser")
    print("=" * 60 + "\n")
    socketio.run(app,
        host="0.0.0.0",
        port=5001,
        debug=True,
        allow_unsafe_werkzeug=True)



