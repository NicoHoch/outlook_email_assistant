import os
from api.azure_graph_api import AzureGraphApiClient

from langgraph_graph.setup_langgraph_graph import build_graph
from models.state import State
import logging


def main():
    email_account = os.getenv("EMAIL_ACCOUNT")

    logging.info("Checking E-Mail Account" + email_account)

    if not email_account:
        logging.info("EMAIL_ACCOUNT environment variable not set.")
        return

    graphClient = AzureGraphApiClient()
    logging.info("Graph Client initialized")

    emails = graphClient.get_unread_emails()
    logging.info(f"Found {len(emails)} new emails")

    if len(emails) == 0:
        logging.info("No new emails found.")
        return

    elif len(emails) > 10:
        logging.info("More than 10 emails found. Skipping processing to save costs.")
        return
    else:
        logging.info(f"Processing {len(emails)} emails")
        graph = build_graph()
        logging.info("Graph initialized")

        for email in emails:
            logging.info(f"Processing email {email['subject']}")
            state = State(email=email, azureGraphClient=graphClient)
            graph.invoke(state)
