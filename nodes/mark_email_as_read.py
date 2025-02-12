from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging


def mark_email_as_read(state: State):
    logging.info("Marking email as read")

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    azureGraphClient.mark_email_as_read(emailId)
