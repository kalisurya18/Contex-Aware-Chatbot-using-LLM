# EduBot – Context-Aware Chatbot for Educational Institutions

An AI-powered educational chatbot that answers questions using institutional information and conversation context. The application supports document-based knowledge retrieval and locally hosted language models through Ollama.

## Project Demonstration

[Watch the project video](https://drive.google.com/file/d/1xLTH8xVUMtqN1FDCpKGdG7EZbdUR7WU9/view?usp=sharing)

## Features

- Answers questions about academics, admissions, placements, library services and scholarships.
- Uses institutional knowledge and uploaded documents to ground responses.
- Supports follow-up questions using conversation context.
- Stores conversation history.
- Provides a responsive chat interface with dark and light themes.
- Runs locally using Ollama.

## Technology Stack

- **Backend:** Python, Flask, Flask-SocketIO
- **AI:** Ollama, local LLMs, Retrieval-Augmented Generation (RAG)
- **Knowledge retrieval:** ChromaDB
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## How It Works

1. A user submits a question through the chat interface.
2. The application searches institutional information and indexed documents for relevant context.
3. The question and retrieved context are sent to the configured local language model.
4. The generated response is returned to the user, with conversation history maintained for follow-up questions.

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/)
- A compatible local model, for example `llama3.2`

## Run Locally

```bash
git clone https://github.com/kalisurya18/Contex-Aware-Chatbot-using-LLM.git
cd Contex-Aware-Chatbot-using-LLM
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install the dependencies listed in the repository's `requirements.txt`:

```bash
pip install -r requirements.txt
```

Start Ollama and download the model configured by the application:

```bash
ollama pull llama3.2
ollama serve
```

In another terminal, start the Flask application using the entry-point documented in the repository (for example, `python app.py`), then open the local address printed in the terminal.

## Project Structure

The application is organized around a Flask backend, frontend templates and static assets, utility modules for database and retrieval operations, and a knowledge base for institutional information. Refer to the source folders for the current implementation.

## Credits

This repository's existing source documentation credits Sudip Nayak. Please retain accurate contributor attribution and update it only to reflect the actual contributions made by each project member.
