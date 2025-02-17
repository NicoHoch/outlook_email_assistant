from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging


def move_email_to_invoices(state: State):
    logging.info("Moving E-Mail to folder: werbung")

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    new_emailId = azureGraphClient.move_email(
        emailId,
        "4. rechnungen",
    )

    if new_emailId:
        state["email"]["id"] = new_emailId

    return state
