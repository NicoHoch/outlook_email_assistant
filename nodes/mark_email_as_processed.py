from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging


def mark_email_as_processed(state: State):
    logging.info("Marking email as processed")

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    result = azureGraphClient.mark_email_as_processed(emailId)

    logging.info(result)

    return
