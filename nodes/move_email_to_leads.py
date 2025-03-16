from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging


def move_email_to_leads(state: State):
    logging.info("Moving E-Mail to folder: leads‚")

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    new_emailId = azureGraphClient.move_email(
        emailId,
        "6. leads",
    )

    if new_emailId:
        state["email"]["id"] = new_emailId

    return state
