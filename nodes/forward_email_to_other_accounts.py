from api.google_sheets_api import GoogleSheetsAPI
from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import logging
import os


def forward_email_to_other_accounts(state: State):
    logging.info("Forwarding Email")

    spreadsheet_id = os.getenv("CALENDAR_ACCOUNTS_SPREADSHEET_ID")
    range_name = "Tabellenblatt1!A:A"

    googleSheetsClient = GoogleSheetsAPI()
    calendar_accounts = googleSheetsClient.read_file(spreadsheet_id, range_name)

    print(calendar_accounts)

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    for calendar_account in calendar_accounts:
        azureGraphClient.forwardEmail(emailId, calendar_account[0])

    return
