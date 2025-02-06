from api.google_vision_ai_api import detect_text
from models.state import State
from api.azure_graph_api import AzureGraphApiClient


def extract_email_attachements(state: State):
    # dwonload email attachments

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    attachments = azureGraphClient.list_attachments(emailId)

    for attachment in attachments:
        mimetype = attachment["contentType"]

        content_bytes = azureGraphClient.download_email_attachment(
            state["email"]["id"], attachment["id"]
        )

        content_str = detect_text(content_bytes)

    # read content of invoice
    # add invoice details to excel file
    # add invoice to google drve
    # move email to folder
    print(state["email"]["sentDateTime"])
