from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY Umgebungsvariable ist nicht gesetzt")
        self.client = ChatOpenAI(api_key=api_key)

    def call_openai(self, messages, model="gpt-4o-mini", response_format=None):
        """
        Calls the OpenAI API with the given messages and model.

        Args:
            messages (list): A list of message dictionaries to send to the OpenAI API.
            model (str, optional): The model to use for the API call. Defaults to "gpt-4o-mini".
            response_format (str, optional): The format of the response. Defaults to None.

        Returns:
            str: The response from the OpenAI API, or None if an error occurred.
        """

        try:
            completion = self.client.invoke(
                model=model, input=messages, response_format=response_format
            )
            return completion.content
        except Exception as e:
            print(f"Fehler bei der API-Anfrage: {e}")
            return None
