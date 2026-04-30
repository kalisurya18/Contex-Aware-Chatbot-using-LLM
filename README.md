
# EduBot - Context-Aware Chatbot for Educational Institutions

<div align="center">

```
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║        🎓  E D U B O T                          ║
    ║                                                  ║
    ║   Context-Aware AI Chatbot for Education         ║
    ║   Powered by Ollama LLMs                         ║
    ║                                                  ║
    ║   Built by: Sudip Nayak (AIML)                    ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
```

**An intelligent AI-powered chatbot that answers questions about your college/university
using real institutional data — courses, admissions, placements, library, and more.**

</div>

---

## What Does This Project Do?

Imagine you're a new student at a college and you have hundreds of questions:

- *"What is the fee structure?"*
- *"When do admissions start?"*
- *"What companies come for placements?"*
- *"How many books can I borrow from the library?"*

Instead of searching through multiple websites or calling different offices,
you simply **type your question** and the chatbot **instantly gives you an accurate answer** — just like chatting with a helpful senior who knows everything about the college!

### How is it "Context-Aware"?

Unlike a normal chatbot that gives generic answers, EduBot is **smart** because:

1. **It knows your institution** — It comes pre-loaded with data about departments, fees, placements, faculty, etc.
2. **You can feed it documents** — Upload your college prospectus, syllabus PDFs, or policy documents, and it will **learn from them** to give even better answers.
3. **It remembers your conversation** — It understands follow-up questions (e.g., you ask "Tell me about CSE" and then "What are its specializations?" — it knows you're still talking about CSE).

---

## How Does It Work? (Simple Explanation)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   You type a question                                           │
│        ↓                                                        │
│   EduBot searches its Knowledge Base for relevant info          │
│        ↓                                                        │
│   It sends your question + relevant context to the AI model     │
│        ↓                                                        │
│   The AI model (running on YOUR computer via Ollama) thinks     │
│        ↓                                                        │
│   You get an accurate, context-aware answer!                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Technology Used:**
| Component | What It Is | Why We Use It |
|-----------|-----------|---------------|
| **Python (Flask)** | A programming language & web framework | Runs the backend server |
| **Ollama** | A tool that runs AI models locally on your computer | Powers the AI brain — no internet/API key needed! |
| **RAG (Retrieval-Augmented Generation)** | A technique to feed relevant documents to AI | Makes answers accurate using real institutional data |
| **SQLite** | A lightweight database | Stores conversation history |
| **HTML/CSS/JavaScript** | Web technologies | Creates the beautiful chat interface you see |

---

## Features

| Feature | What It Does |
|---------|-------------|
| AI Chat | Ask any question about the institution and get smart answers |
| Context-Aware | Uses real institutional data (not generic responses) |
| Document Upload | Upload PDFs, Word docs, or text files to teach the bot more |
| 6 Categories | Filter by Academics, Admissions, Placements, Library, Scholarships |
| Chat History | All your conversations are saved — come back anytime |
| Dark/Light Theme | Switch between cool dark mode and clean light mode |
| Smart Suggestions | Pre-made questions to get you started quickly |
| Copy & Feedback | Copy any answer or rate it with thumbs up/down |
| Responsive | Works beautifully on phones, tablets, and desktops |
| 100% Offline | Runs entirely on your computer — no data sent to the cloud |

---

## Prerequisites (What You Need to Install First)

Before running EduBot, you need **two things** installed on your computer:

### 1. Python (version 3.8 or higher)

Python is the programming language this project is written in.

**Check if you already have Python:**
Open your Terminal (Mac/Linux) or Command Prompt (Windows) and type:
```bash
python3 --version
```
If you see something like `Python 3.10.12`, you're good! If not, install it:

| Operating System | How to Install |
|-----------------|----------------|
| **Windows** | Go to [python.org/downloads](https://www.python.org/downloads/), download the installer, run it. **IMPORTANT: Check the box "Add Python to PATH" during installation!** |
| **Mac** | Open Terminal and run: `brew install python3` (if you have Homebrew) OR download from [python.org/downloads](https://www.python.org/downloads/) |
| **Linux (Ubuntu)** | Open Terminal and run: `sudo apt update && sudo apt install python3 python3-pip python3-venv` |

### 2. Ollama (the AI engine)

Ollama is what runs the AI model on your computer. It's free and easy to install.

**Install Ollama:**

| Operating System | How to Install |
|-----------------|----------------|
| **Windows** | Go to [ollama.com](https://ollama.com), click Download, run the installer |
| **Mac** | Go to [ollama.com](https://ollama.com), click Download, drag to Applications. OR run: `brew install ollama` |
| **Linux** | Open Terminal and run: `curl -fsSL https://ollama.com/install.sh \| sh` |

**After installing Ollama, download an AI model:**

Open your Terminal/Command Prompt and run:
```bash
ollama pull llama3.2
```

This downloads a ~2GB AI model to your computer. It only needs to be done once.
Wait for it to finish (it may take a few minutes depending on your internet speed).

> **Note:** If your computer has less than 8GB RAM, use a smaller model instead:
> ```bash
> ollama pull phi3
> ```
> Then change the model name in `config.py` (explained in Configuration section below).

---

## How to Run the Project (Step-by-Step)

### Step 1: Download the Project

If you received this as a ZIP file, extract it to a folder on your computer.

If you're using Git:
```bash
git clone <repository-url>
cd edu-chatbot
```

### Step 2: Start Ollama

Open a **new Terminal/Command Prompt window** and run:
```bash
ollama serve
```
Keep this window open! Ollama needs to be running in the background.

> **On Mac:** If you installed Ollama as an app, just open it from Applications — it runs automatically in the background.

### Step 3: Run EduBot

**Option A — Easy Way (Mac/Linux):**
```bash
cd edu-chatbot
chmod +x run.sh
./run.sh
```

**Option B — Manual Way (All Operating Systems):**

```bash
# Navigate to the project folder
cd edu-chatbot

# Create a virtual environment (isolates project dependencies)
python3 -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install flask flask-socketio requests werkzeug gevent gevent-websocket

# Run the application
python3 app.py
```

### Step 4: Open in Browser

Once you see the message:
```
============================================================
  EduBot - Context-Aware Educational Chatbot
============================================================
  Open http://localhost:5000 in your browser
============================================================
```

Open your web browser (Chrome, Firefox, Edge, Safari) and go to:

```
http://localhost:5000
```

You should see the beautiful EduBot interface! Start chatting!

### Step 5: To Stop the Application

- Press `Ctrl + C` in the Terminal where the app is running
- Close the Ollama window too (or press `Ctrl + C` there)

---

## How to Use EduBot

### Asking Questions
Simply type your question in the text box at the bottom and press **Enter** or click the **Send** button.

**Example questions you can ask:**
- "What departments are available?"
- "Tell me about the B.Tech admission process"
- "What is the fee structure per semester?"
- "Which companies come for campus placements?"
- "What are the library timings?"
- "Are there any scholarships available?"
- "What clubs can I join?"
- "What is the minimum attendance requirement?"

### Using Categories
Click on category pills in the sidebar (**Academics**, **Admissions**, **Placements**, etc.) to get more targeted responses and relevant suggestion cards.

### Uploading Documents
Want EduBot to know about specific information? Click **Upload Docs** in the header, then:
1. Select a PDF, Word document, or text file
2. Choose a category
3. Click **Upload & Index**

The chatbot will now use that document's content to answer questions more accurately!

### Conversation History
Your chats are automatically saved. Click on any previous conversation in the sidebar to continue it.

### Dark/Light Mode
Click the sun/moon icon at the bottom of the sidebar to switch themes.

---

## Project Structure (For Developers)

```
edu-chatbot/
│
├── app.py                        ← Main application (Flask server + API routes)
├── config.py                     ← Settings (model name, paths, system prompt)
├── requirements.txt              ← List of Python packages needed
├── run.sh                        ← One-click startup script (Mac/Linux)
│
├── templates/
│   └── index.html                ← The web page (chat interface)
│
├── static/
│   ├── css/
│   │   └── style.css             ← All the styling (dark theme, animations, layout)
│   └── js/
│       └── app.js                ← Frontend logic (sending messages, UI updates)
│
├── utils/
│   ├── __init__.py               ← Makes 'utils' a Python package
│   ├── db.py                     ← Database operations (save/load conversations)
│   ├── ollama_client.py          ← Talks to the Ollama AI model
│   └── rag.py                    ← RAG engine (processes and searches documents)
│
├── knowledge_base/
│   └── institution_data.json     ← Pre-loaded institution data (editable!)
│
├── uploads/                      ← Uploaded documents are stored here
└── README.md                     ← This file!
```

---

## Configuration (Changing Settings)

### Changing the AI Model

Open `config.py` and change the `OLLAMA_MODEL` value:

```python
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
#                                                ^^^^^^^^
#                                        Change this to any model you have
```

**Popular models you can use:**
| Model | Size | Best For |
|-------|------|----------|
| `llama3.2` | ~2GB | General use (recommended) |
| `llama3.2:1b` | ~1.3GB | Low-RAM computers |
| `mistral` | ~4GB | Good quality responses |
| `phi3` | ~2GB | Fast, lightweight |
| `gemma2` | ~5GB | High quality |

Remember to pull the model first:
```bash
ollama pull <model-name>
```

### Customizing Institution Data

The file `knowledge_base/institution_data.json` contains all the institution information.
Open it in any text editor and replace the data with your actual college/university details:

- Institution name, address, website
- Department names, HODs, programs
- Fee structure, admission process
- Placement statistics
- Library details
- Scholarships
- And more!

The chatbot automatically loads this data when it starts.

---

## Troubleshooting (Common Problems & Solutions)

### "Cannot connect to Ollama"
**Problem:** The chatbot shows "Ollama offline" in the sidebar.
**Solution:**
1. Make sure Ollama is running. Open a terminal and run: `ollama serve`
2. Make sure you've downloaded a model: `ollama pull llama3.2`
3. Check if Ollama is accessible: open `http://localhost:11434` in your browser — you should see "Ollama is running"

### "Module not found" error
**Problem:** You see `ModuleNotFoundError` when running `python3 app.py`
**Solution:**
```bash
# Make sure your virtual environment is activated
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies again
pip install flask flask-socketio requests werkzeug
```

### "Port 5000 already in use"
**Problem:** Another application is using port 5000.
**Solution:** Close the other application, or change the port in `app.py`:
```python
socketio.run(app, host="0.0.0.0", port=8080, debug=True)
#                                       ^^^^
#                               Change to any free port
```
Then open `http://localhost:8080` instead.

### Slow responses
**Problem:** The AI takes too long to respond.
**Solution:**
- Use a smaller/faster model: `ollama pull phi3` and update `config.py`
- Close other heavy applications to free up RAM
- The first response is always slower (model loading). Subsequent ones are faster.

### "Address already in use" on Mac
**Problem:** macOS AirPlay Receiver uses port 5000 by default.
**Solution:** Go to System Settings > General > AirDrop & Handoff > turn off AirPlay Receiver. OR change the port as shown above.

---

## Tech Stack Summary

```
┌────────────────────────────────────────────────┐
│                 FRONTEND                        │
│  HTML5 + CSS3 + Vanilla JavaScript              │
│  (Dark/Light themes, animations, responsive)    │
├────────────────────────────────────────────────┤
│                 BACKEND                         │
│  Python Flask + Flask-SocketIO                  │
│  (REST API + WebSocket for streaming)           │
├────────────────────────────────────────────────┤
│               AI ENGINE                         │
│  Ollama (Local LLM) + RAG Pipeline              │
│  (Context-aware responses using documents)      │
├────────────────────────────────────────────────┤
│               DATABASE                          │
│  SQLite (conversations, messages, feedback)     │
│  ChromaDB (document vector storage for RAG)     │
└────────────────────────────────────────────────┘
```

---

## API Endpoints (For Developers)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the main chat interface |
| `GET` | `/api/status` | Check Ollama connection status |
| `GET` | `/api/conversations` | List all saved conversations |
| `POST` | `/api/conversations` | Create a new conversation |
| `DELETE` | `/api/conversations/<id>` | Delete a conversation |
| `GET` | `/api/conversations/<id>/messages` | Get messages for a conversation |
| `POST` | `/api/chat` | Send a message and get AI response |
| `POST` | `/api/upload` | Upload a document for RAG indexing |
| `GET` | `/api/documents` | List all uploaded documents |
| `POST` | `/api/feedback` | Submit feedback (like/dislike) |
| `GET` | `/api/suggestions?category=X` | Get suggested questions |

---

## Credits

- **Developer:** Sudip Nayak (AIML)
- **AI Engine:** [Ollama](https://ollama.com) — Run LLMs locally
- **Framework:** [Flask](https://flask.palletsprojects.com/) — Python web framework
- **RAG:** Retrieval-Augmented Generation for context-aware responses

---

<div align="center">

**Built with passion for education.**

*If you have questions or issues, feel free to reach out!*

</div>
