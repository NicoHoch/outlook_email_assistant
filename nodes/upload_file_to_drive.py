from api.google_drive_api import GoogleDriveAPI
from models.state import State
import os
import base64
import logging


def upload_file_to_drive(state: State):
    logging.info("Uploading file to Google Drive")

    googleDriveClient = GoogleDriveAPI()

    # Google Sheet ID and range (e.g., "Sheet1!A1" to start at the top left)
    folder_id = os.getenv("INVOICE_FOLDER_ID")

    for attachment in state["attachments"]:

        content_base64 = attachment.get("contentBytes")
        content_bytes = base64.b64decode(content_base64)

        json_data = attachment["json_data"]
        filename = (
            json_data["invoice_date"]
            + "_"
            + json_data["vendor_name"]
            + attachment["name"]
        )

        file_link = googleDriveClient.upload_file(folder_id, filename, content_bytes)
        attachment["file_link"] = file_link

    return state
