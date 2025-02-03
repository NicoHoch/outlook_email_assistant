from openai import OpenAI
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen
load_dotenv()


class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY Umgebungsvariable ist nicht gesetzt")
        self.client = OpenAI(api_key=api_key)

    def call_openai(self, message, model="gpt-4o-mini", store=True):
        try:
            completion = self.client.chat.completions.create(
                model=model,
                store=store,
                messages=[{"role": "user", "content": message}],
            )
            return completion.choices[0].message
        except Exception as e:
            print(f"Fehler bei der API-Anfrage: {e}")
            return None
