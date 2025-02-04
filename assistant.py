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
    emails = graphClient.get_unread_emails(email_account)

    graph = build_graph()

    for email in emails:
        state = State(email=email)
        graph.invoke(state)


if __name__ == "__main__":
    main()
