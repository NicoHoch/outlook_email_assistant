import os
from dotenv import load_dotenv
from api.graph_api import GraphApiClient


def main():
    load_dotenv()
    email_account = os.getenv("EMAIL_ACCOUNT")

    if not email_account:
        print("EMAIL_ACCOUNT environment variable not set.")
        return

    graphClient = GraphApiClient()
    emails = graphClient.get_unread_emails(email_account)

    for email in emails:
        print(email["subject"])


if __name__ == "__main__":
    main()
