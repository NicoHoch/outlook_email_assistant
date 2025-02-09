from api.google_vision_ai_api import detect_text_from_image
from models.state import State
from api.azure_graph_api import AzureGraphApiClient


def extract_email_attachments(state: State):

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    attachments = azureGraphClient.list_attachments(emailId)

    return {"attachments": attachments}
