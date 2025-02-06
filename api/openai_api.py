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
        """
        Calls the OpenAI API with the given message and model.

        Args:
            message (str): The message to send to the OpenAI API.
            model (str, optional): The model to use for the API call. Defaults to "gpt-4o-mini".
            store (bool, optional): Whether to store the conversation. Defaults to True.

        Returns:
            str: The response from the OpenAI API, or None if an error occurred.
        """
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
