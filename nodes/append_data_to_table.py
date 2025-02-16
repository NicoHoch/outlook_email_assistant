from api.google_sheets_api import GoogleSheetsAPI
from models.state import State
import os
import logging


def append_data_to_table(state: State):

    logging.info("Appending data to Google Sheet")

    googleSheetsClient = GoogleSheetsAPI()

    # Google Sheet ID and range (e.g., "Sheet1!A1" to start at the top left)
    spreadsheet_id = os.getenv("EXPENDITURE_SPREADSHEET_ID")
    range_name = "Tabellenblatt1!A1"  # Replace with the range where you want to insert

    for attachment in state["attachments"]:

        json_data = attachment["json_data"]

        values = [
            state["email"]["receivedDateTime"],
            json_data["invoice_date"],
            json_data["products"],
            json_data["vendor_name"],
            json_data["total_price"],
            attachment["file_link"],
        ]

        googleSheetsClient.insert_row(spreadsheet_id, range_name, values)
