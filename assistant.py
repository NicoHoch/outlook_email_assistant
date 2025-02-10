import os
from dotenv import load_dotenv
from api.azure_graph_api import AzureGraphApiClient

from langgraph_graph.setup_langgraph_graph import build_graph
from models.state import State


def main():
    load_dotenv()
    email_account = os.getenv("EMAIL_ACCOUNT")

    if not email_account:
        print("EMAIL_ACCOUNT environment variable not set.")
        return

    graphClient = AzureGraphApiClient()

    emails = graphClient.get_unread_emails()

    if len(emails) == 0:
        print("No new emails found.")
        return

    elif len(emails) > 10:
        raise Exception(
            f"{len(emails)} emails found. Too many emails to process at once."
        )

    graph = build_graph()

    for email in emails:
        state = State(email=email, azureGraphClient=graphClient)
        graph.invoke(state)


if __name__ == "__main__":
    main()
