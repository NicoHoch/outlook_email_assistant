import os
from dotenv import load_dotenv

from api.graph_api import GraphApiClient

load_dotenv()

email_account = os.getenv("EMAIL_ACCOUNT")

graphClient = GraphApiClient()

emails = graphClient.get_unred_emails(email_account)
