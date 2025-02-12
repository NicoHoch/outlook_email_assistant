import json
from dotenv import load_dotenv
import os
from msal import ConfidentialClientApplication
import requests

# Lade Umgebungsvariablen
load_dotenv()


class AzureGraphApiClient:
    def __init__(self):
        self.email_account = os.getenv("EMAIL_ACCOUNT")
        clientId = os.getenv("AZURE_CLIENT_ID")
        TenantId = os.getenv("AZURE_TENANT_ID")
        clientSecret = os.getenv("AZURE_CLIENT_SECRET")

        # Microsoft Graph API Endpoint for E-Mails
        graphApiEndpoint = (
            f"https://graph.microsoft.com/v1.0/users/{self.email_account}/messages"
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

    def get_unread_emails(self) -> dict:
        """
        Fetches unread emails for the specified email account.

        Args:
            email_account (str): The email account to fetch unread emails from.

        Returns:
            dict: A dictionary containing the unread emails.
        """
        graphApiEndpoint = f"https://graph.microsoft.com/v1.0/users/{self.email_account}/messages?$filter=isRead eq false"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        # Request to Graph API for unread emails
        response = requests.get(graphApiEndpoint, headers=headers)

        if response.status_code == 200:
            emails = response.json().get("value", [])
        else:
            print("Error when accessing the Graph API:", response.text)
            emails = []

        return emails

    def list_attachments(self, email_id):
        """
        Lists attachments for the specified email account and email ID.

        Args:
            email_account (str): The email account to list attachments from.
            email_id (str): The ID of the email to list attachments for.

        Returns:
            dict: A dictionary containing the attachments for the specified email.
        """
        graphApiEndpoint = f"https://graph.microsoft.com/v1.0/users/{self.email_account}/messages/{email_id}/attachments"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(graphApiEndpoint, headers=headers)

        if response.status_code == 200:
            attachments = response.json().get("value", [])
        else:
            print("Error when accessing the Graph API:", response.text)
            attachments = []

        return attachments

    def download_email_attachment(self, email_id, attachment_id):
        """
        Downloads an email attachment for the specified email account and email ID.

        Args:
            email_account (str): The email account to download the attachment from.
            email_id (str): The ID of the email containing the attachment.
            attachment_id (str): The ID of the attachment to download.
            file_path (str): The local file path to save the downloaded attachment.

        Returns:
            bool: True if the attachment was downloaded successfully, False otherwise.
        """
        graphApiEndpoint = f"https://graph.microsoft.com/v1.0/users/{self.email_account}/messages/{email_id}/attachments/{attachment_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(graphApiEndpoint, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print("Error when accessing the Graph API:", response.text)
            return False

    def mark_email_as_read(self, email_id):
        """
        Marks an email as read for the specified email account and email ID.

        Args:
            email_account (str): The email account to mark the email as read.
            email_id (str): The ID of the email to mark as read.

        Returns:
            bool: True if the email was marked as read successfully, False otherwise.
        """
        graphApiEndpoint = f"https://graph.microsoft.com/v1.0/users/{self.email_account}/messages/{email_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {"isRead": "true"}

        response = requests.patch(
            graphApiEndpoint, headers=headers, data=json.dumps(payload)
        )

        if response.status_code == 200:
            return True
        else:
            print("Error when accessing the Graph API:", response.text)
            return False
