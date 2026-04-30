import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "edu-chatbot-secret-2024")
    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
    DB_PATH = os.path.join(os.path.dirname(__file__), "chatbot.db")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {"pdf", "txt", "docx", "md"}
    CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

    SYSTEM_PROMPT = """You are EduBot, an intelligent and friendly AI assistant for educational institutions.
You help students, faculty, and staff with questions about:
- Academic programs, courses, and curriculum
- Admission procedures and requirements
- Examination schedules and results
- Library resources and facilities
- Campus facilities and services
- Faculty information and office hours
- Student clubs and extracurricular activities
- Scholarships and financial aid
- Administrative procedures and policies
- Career guidance and placement services

IMPORTANT GUIDELINES:
- Be helpful, accurate, and concise
- If you have context documents provided, use them to answer accurately
- If you don't know something specific, say so honestly and suggest where to find the information
- Maintain a professional yet friendly tone
- Format responses with markdown when helpful (lists, bold, etc.)
- For urgent matters, always suggest contacting the relevant department directly
"""
