from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleSheetsAPI:
    def __init__(self):
        # Use the credentials directly from the environment variable
        self.credentials = service_account.Credentials.from_service_account_file(
            "keys/google-credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )

        # Build the Sheets API client
        self.service = build("sheets", "v4", credentials=self.credentials)

    def insert_row(self, spreadsheet_id, range_name, row_data):
        values = [row_data]
        body = {"values": values}

        # Append the row to the sheet
        request = (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body,
            )
        )
        response = request.execute()
        print(f"Row inserted: {response}")

    def read_file(self, spreadsheet_id, range_name):
        # Read the data from the sheet
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        print(f"Data read from sheet: {rows}")
        return rows
