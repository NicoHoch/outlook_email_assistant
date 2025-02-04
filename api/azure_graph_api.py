import json
from dotenv import load_dotenv
import os
from msal import ConfidentialClientApplication
import requests

# Lade Umgebungsvariablen
load_dotenv()


class AzureGraphApiClient:
    def __init__(self):
        clientId = os.getenv("AZURE_CLIENT_ID")
        TenantId = os.getenv("AZURE_TENANT_ID")
        clientSecret = os.getenv("AZURE_CLIENT_SECRET")

        # Microsoft Graph API Endpoint for E-Mails
        graphApiEndpoint = (
            "https://graph.microsoft.com/v1.0/users/{EMAIL_ACCOUNT}/messages"
        )

        # Initialisiere MSAL Client
        app = ConfidentialClientApplication(
            clientId,
            authority=f"https://login.microsoftonline.com/{TenantId}",
            client_credential=clientSecret,
        )

        token_response = app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )

        if "access_token" in token_response:
            self.access_token = token_response["access_token"]
        else:
            print(
                "Error when accessing the token:",
                token_response.get("error_description"),
            )

    def get_unread_emails(self, email_account) -> dict:

        graphApiEndpoint = f"https://graph.microsoft.com/v1.0/users/{email_account}/messages?$filter=isRead eq false"

        headers = {"Authorization": f"Bearer {self.access_token}"}

        # Anfrage an Graph API für ungelesene E-Mails
        response = requests.get(graphApiEndpoint, headers=headers)

        if response.status_code == 200:
            emails = response.json()["value"]
        else:
            print("Error when accessing the Graph API:", response.text)
            emails = []
        return emails
