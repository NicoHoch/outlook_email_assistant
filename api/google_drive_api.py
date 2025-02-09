from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2 import service_account


class GoogleDriveAPI:
    def __init__(self):
        # Use the credentials directly from the environment variable
        self.credentials = service_account.Credentials.from_service_account_file(
            "keys/google-credentials.json",
            scopes=["https://www.googleapis.com/auth/drive.file"],
        )

        self.service = build("drive", "v3", credentials=self.credentials)

    def upload_file(self, folder_id, filename, file_content):

        media = MediaInMemoryUpload(file_content, mimetype="application/octet-stream")

        file_metadata = {"name": filename, "parents": [folder_id]}

        file = (
            self.service.files()
            .create(media_body=media, body=file_metadata, fields="id, webViewLink")
            .execute()
        )

        file_link = file.get("webViewLink")
        print(
            f'File uploaded successfully. File ID: {file["id"]}, File Link: {file_link}'
        )
        return file_link
