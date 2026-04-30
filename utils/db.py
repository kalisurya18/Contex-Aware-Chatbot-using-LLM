import sqlite3

def init_db():
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations 
                 (id TEXT PRIMARY KEY, title TEXT, category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def create_conversation(id, title, category):
    conn = sqlite3.connect('chatbot.db')
    conn.execute("INSERT INTO conversations VALUES (?, ?, ?)", (id, title, category))
    conn.commit()
    conn.close()

def get_conversations():
    conn = sqlite3.connect('chatbot.db')
    conn.row_factory = sqlite3.Row
    convs = conn.execute("SELECT * FROM conversations").fetchall()
    return [dict(row) for row in convs]

def add_message(conv_id, role, content):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", (conv_id, role, content))
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return msg_id

def get_messages(conv_id):
    conn = sqlite3.connect('chatbot.db')
    conn.row_factory = sqlite3.Row
    msgs = conn.execute("SELECT * FROM messages WHERE conversation_id = ?", (conv_id,)).fetchall()
    return [dict(row) for row in msgs]

# Dummy functions for remaining imports in app.py
def delete_conversation(id): pass
def add_feedback(m_id, r, c): pass
def save_document(f, o, c, ch): pass
def get_documents(): return []