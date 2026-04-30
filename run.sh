#!/bin/bash
# ══════════════════════════════════════════════════
#  EduBot - Quick Start Script
# ══════════════════════════════════════════════════

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   🎓 EduBot - Educational AI Chatbot    ║"
echo "  ║   Context-Aware • Ollama Powered         ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required. Install it first."
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q flask flask-socketio requests werkzeug gevent gevent-websocket 2>/dev/null

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama is running"
    else
        echo "⚠️  Ollama is not running. Start it with: ollama serve"
        echo "   Then pull a model: ollama pull llama3.2"
    fi
else
    echo "⚠️  Ollama not found. Install from: https://ollama.ai"
fi

echo ""
echo "🚀 Starting EduBot..."
echo "   Open http://localhost:5000 in your browser"
echo ""

python3 app.py
