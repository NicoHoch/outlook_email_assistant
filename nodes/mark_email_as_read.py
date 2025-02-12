from api.google_vision_ai_api import detect_text_from_image
from models.state import State
from api.azure_graph_api import AzureGraphApiClient


def mark_email_as_read(state: State):

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    azureGraphClient.mark_email_as_read(emailId)
