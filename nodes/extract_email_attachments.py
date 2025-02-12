from api.google_vision_ai_api import detect_text_from_image
from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging


def extract_email_attachments(state: State):
    logging.info("Extracting email attachments")

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    attachments = azureGraphClient.list_attachments(emailId)

    if len(attachments) >= 3:
        raise Exception(
            "Please check the email account. More than 3 attachments found."
        )

    return {"attachments": attachments}
