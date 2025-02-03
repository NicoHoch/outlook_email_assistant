import os
import json
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration aus Umgebungsvariablen
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# Microsoft Graph API Endpoint für E-Mails
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/users/{EMAIL_ACCOUNT}/messages"


# Initialisiere MSAL Client
app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)

# Erhalte ein Token für die Graph API
token_response = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" in token_response:
    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Anfrage an Graph API für E-Mails
    response = requests.get(GRAPH_API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        emails = response.json()
        print(json.dumps(emails, indent=2))
    else:
        print(f"Fehler beim Abruf der E-Mails: {response.status_code}, {response.text}")
else:
    print(
        "Fehler bei der Token-Autorisierung:", token_response.get("error_description")
    )
