import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def check_connection(self):
        try:
            response = requests.get(self.base_url)
            return response.status_code == 200
        except:
            return False

    def list_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return [m['name'] for m in response.json().get('models', [])]
        except:
            return ["llama3"]

    def generate_response(self, messages, context=None):
        if context:
            system_message = {
                "role": "system",
                "content": f"""
        You are EduBot for Pragati Engineering College.

        Answer ONLY using the institutional data below.

        Institution Data:
        {context}
        """
            }

            messages = [system_message] + messages
        payload = {
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=300
            )

            data = response.json()
            print("OLLAMA RESPONSE:", data)   # optional debug

            # ✅ SAFE parsing
            if "message" in data and isinstance(data["message"], dict):
                reply = data["message"].get("content", "")

            elif "response" in data:
                reply = data["response"]

            elif "error" in data:
                return {
                    "success": False,
                    "response": f"Ollama Error: {data['error']}"
                }

            else:
                reply = "No response from model"

            return {
                "success": True,
                "response": reply,
                "model": data.get("model", "llama3.2")
            }

        except Exception as e:
            return {
                "success": False,
                "response": f"Ollama Error: {str(e)}"
            }

    def stream_response(self, messages, context=None):
        # Basic placeholder for streaming
        yield "Processing your request..."