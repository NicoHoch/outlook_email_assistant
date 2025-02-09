import json
from api.openai_api import OpenAIClient
from models.state import State


def extract_structured_data(state: State) -> dict:
    """
    Extracts structured data from the attachments in the given state.

    Args:
        state (State): The state object containing attachments.

    Returns:
        dict: A dictionary containing the extracted structured data or error messages.
    """

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "invoice_format",
            "schema": {
                "type": "object",
                "properties": {
                    "vendor_name": {"type": "string"},
                    "invoice_date": {"type": "string"},
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product": {"type": "string"},
                                "price": {"type": "number"},
                            },
                            "total_price": {"type": "number"},
                        },
                    },
                },
            },
        },
    }

    for attachment in state["attachments"]:
        messages = [
            {
                "role": "system",
                "content": "Extract structured data from the content provided and return it in JSON format.",
            },
            {"role": "user", "content": attachment["contentStr"]},
        ]

        openai_client = OpenAIClient()

        result = openai_client.call_openai(
            messages, model="gpt-4o-mini", response_format=response_format
        )

        try:
            json_result = json.loads(result)
        except json.JSONDecodeError:
            json_result = {"error": "Failed to decode JSON"}

        attachment["json_data"] = json_result

    return state
