import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)
model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def _extract_json(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

def get_llm_response(system_prompt: str, user_input: dict) -> str:
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_input)}
        ]
        try:
            response = client.chat.completions.create(
                model=model_name,
                temperature=0,
                response_format={"type": "json_object"},
                messages=messages
            )
        except Exception:
            response = client.chat.completions.create(
                model=model_name,
                temperature=0,
                messages=messages
            )
        content = response.choices[0].message.content or ""
        return _extract_json(content)
    except Exception as e:
        # In a real-world scenario, you might want to add more robust error handling and retries.
        print(f"Error calling Groq API: {e}")
        return ""
