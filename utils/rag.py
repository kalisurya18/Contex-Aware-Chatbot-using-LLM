# import os
# import json
# import uuid
# from typing import List, Optional

# import chromadb
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer

# from config import Config


# class RAGEngine:
#     def __init__(self):
#         # Initialize embedding model
#         self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

#         # Initialize ChromaDB persistent client
#         self.client = chromadb.Client(
#             Settings(
#                 persist_directory=Config.CHROMA_PERSIST_DIR,
#                 anonymized_telemetry=False
#             )
#         )

#         # Create or get collection
#         self.collection = self.client.get_or_create_collection(
#             name="edu_documents"
#         )

#         # Ensure directory exists
#         os.makedirs(Config.CHROMA_PERSIST_DIR, exist_ok=True)

#         # Load institution JSON on startup
#         self._load_institution_data()

#     # ─────────────────────────────────────────────
#     # Load institution_data.json automatically
#     # ─────────────────────────────────────────────
#     def _load_institution_data(self):
#         kb_path = os.path.join(
#             Config.KNOWLEDGE_BASE_DIR,
#             "institution_data.json"
#         )

#         if not os.path.exists(kb_path):
#             return

#         with open(kb_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         # Convert JSON to readable text
#         text_content = json.dumps(data)

#         # Add to vector DB
#         self._add_chunks(
#             text_content,
#             metadata={
#                 "source": "institution_data.json",
#                 "category": "general"
#             }
#         )

#     # ─────────────────────────────────────────────
#     # Add document
#     # ─────────────────────────────────────────────
#     def add_document(self, filepath: str, original_name: str, category: str):
#         text = self._extract_text(filepath)
#         if not text.strip():
#             return 0

#         chunks = self._chunk_text(text)

#         self._add_chunks(
#             chunks,
#             metadata={
#                 "source": original_name,
#                 "category": category
#             }
#         )

#         return len(chunks)

#     # ─────────────────────────────────────────────
#     # Search
#     # ─────────────────────────────────────────────
#     def search(self, query: str, n_results: int = 3, category: Optional[str] = None):
#         if self.collection.count() == 0:
#             return ""

#         query_embedding = self.embedding_model.encode(query).tolist()

#         where_filter = None
#         if category:
#             where_filter = {"category": category}

#         results = self.collection.query(
#             query_embeddings=[query_embedding],
#             n_results=n_results,
#             where=where_filter
#         )

#         documents = results.get("documents", [[]])[0]

#         if not documents:
#             return ""

#         return "\n\n".join(documents)

#     # ─────────────────────────────────────────────
#     # Internal: Add chunks to Chroma
#     # ─────────────────────────────────────────────
#     def _add_chunks(self, text_or_chunks, metadata):
#         if isinstance(text_or_chunks, str):
#             chunks = self._chunk_text(text_or_chunks)
#         else:
#             chunks = text_or_chunks

#         ids = [str(uuid.uuid4()) for _ in chunks]
#         embeddings = self.embedding_model.encode(chunks).tolist()

#         metadatas = [metadata for _ in chunks]

#         self.collection.add(
#             documents=chunks,
#             embeddings=embeddings,
#             metadatas=metadatas,
#             ids=ids
#         )

#     # ─────────────────────────────────────────────
#     # Text Extraction
#     # ─────────────────────────────────────────────
#     def _extract_text(self, filepath):
#         ext = filepath.split(".")[-1].lower()

#         try:
#             if ext == "txt" or ext == "md":
#                 with open(filepath, "r", encoding="utf-8") as f:
#                     return f.read()

#             elif ext == "pdf":
#                 import PyPDF2
#                 text = ""
#                 with open(filepath, "rb") as f:
#                     reader = PyPDF2.PdfReader(f)
#                     for page in reader.pages:
#                         text += page.extract_text() or ""
#                 return text

#             elif ext == "docx":
#                 import docx
#                 doc = docx.Document(filepath)
#                 return "\n".join([p.text for p in doc.paragraphs])

#         except Exception as e:
#             print("Text extraction error:", e)
#             return ""

#         return ""

#     # ─────────────────────────────────────────────
#     # Chunking Logic
#     # ─────────────────────────────────────────────
#     def _chunk_text(self, text, chunk_size=500, overlap=100):
#         chunks = []
#         start = 0
#         length = len(text)

#         while start < length:
#             end = start + chunk_size
#             chunk = text[start:end]
#             chunks.append(chunk)
#             start += chunk_size - overlap

#         return chunks



import os
import json
import uuid
from typing import Optional, List, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from config import Config


class RAGEngine:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.Client(
            Settings(
                persist_directory=Config.CHROMA_PERSIST_DIR,
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="universal_documents"
        )

        os.makedirs(Config.CHROMA_PERSIST_DIR, exist_ok=True)

        self._load_all_json_files()

    # ─────────────────────────────────────────────
    # LOAD ALL JSON FILES (GENERIC)
    # ─────────────────────────────────────────────
    def _load_all_json_files(self):
        kb_dir = Config.KNOWLEDGE_BASE_DIR

        if not os.path.exists(kb_dir):
            return

        for file in os.listdir(kb_dir):
            if file.endswith(".json"):
                path = os.path.join(kb_dir, file)
                self._index_json_file(path, file)

    # ─────────────────────────────────────────────
    # INDEX ANY JSON FILE
    # ─────────────────────────────────────────────
    def _index_json_file(self, filepath: str, filename: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []
        metadatas = []
        ids = []

        # Recursively flatten JSON
        flattened_entries = self._flatten_json(data)

        for entry in flattened_entries:
            documents.append(entry)
            metadatas.append({"source": filename})
            ids.append(str(uuid.uuid4()))

        embeddings = self.embedding_model.encode(documents).tolist()

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    # ─────────────────────────────────────────────
    # RECURSIVE JSON FLATTENER
    # Converts ANY nested JSON into semantic entries
    # ─────────────────────────────────────────────
    def _flatten_json(self, data: Any, parent_key: str = "") -> List[str]:
        entries = []

        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                entries.extend(self._flatten_json(value, new_key))

        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_key = f"{parent_key}[{i}]"
                entries.extend(self._flatten_json(item, new_key))

        else:
            # Leaf node
            entry = f"{parent_key}: {data}"
            entries.append(entry)

        return entries

    # ─────────────────────────────────────────────
    # UNIVERSAL SEARCH
    # No fixed limit — retrieves everything and filters
    # ─────────────────────────────────────────────
    def search(self, query: str):
        total_docs = self.collection.count()

        if total_docs == 0:
            return ""

        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=total_docs  # retrieve ALL indexed docs
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return ""

        # Dynamic similarity filtering (adaptive)
        relevant_docs = []
        threshold = min(distances) + 0.25 if distances else None

        for doc, dist in zip(documents, distances):
            if threshold is None or dist <= threshold:
                relevant_docs.append(doc)

        return "\n".join(relevant_docs)

    # ─────────────────────────────────────────────
    # ADD EXTERNAL DOCUMENTS (PDF/TXT/DOCX)
    # ─────────────────────────────────────────────
    def add_document(self, filepath: str, original_name: str):
        text = self._extract_text(filepath)

        if not text.strip():
            return 0

        chunks = self._chunk_text(text)

        ids = [str(uuid.uuid4()) for _ in chunks]
        embeddings = self.embedding_model.encode(chunks).tolist()
        metadatas = [{"source": original_name} for _ in chunks]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        return len(chunks)

    # ─────────────────────────────────────────────
    # TEXT EXTRACTION
    # ─────────────────────────────────────────────
    def _extract_text(self, filepath):
        ext = filepath.split(".")[-1].lower()

        try:
            if ext in ["txt", "md"]:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()

            elif ext == "pdf":
                import PyPDF2
                text = ""
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or ""
                return text

            elif ext == "docx":
                import docx
                doc = docx.Document(filepath)
                return "\n".join([p.text for p in doc.paragraphs])

        except Exception as e:
            print("Extraction error:", e)

        return ""

    # ─────────────────────────────────────────────
    # SMART CHUNKING
    # ─────────────────────────────────────────────
    def _chunk_text(self, text, chunk_size=800, overlap=150):
        chunks = []
        start = 0
        length = len(text)

        while start < length:
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap

        return chunks