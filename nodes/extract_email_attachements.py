from api.google_vision_ai_api import detect_text_from_image
from models.state import State
from api.azure_graph_api import AzureGraphApiClient
import base64
import fitz  # PyMuPDF


def extract_email_attachements(state: State):
    # dwonload email attachments

    emailId = state["email"]["id"]

    azureGraphClient: AzureGraphApiClient = state["azureGraphClient"]

    attachments = azureGraphClient.list_attachments(emailId)

    for attachment in attachments:
        mimetype = attachment["contentType"]

        if mimetype == "image/jpeg":
            content_base64 = attachment.get("contentBytes")

            if content_base64:
                # Decode Base64 string to raw bytes
                content_bytes = base64.b64decode(content_base64)
            else:
                raise ValueError("No contentBytes found in the attachment!")

            content_str = detect_text_from_image(content_bytes)

        elif mimetype == "application/pdf":
            content_base64 = attachment.get("contentBytes")

            if content_base64:
                # Decode Base64 string to raw bytes
                content_bytes = base64.b64decode(content_base64)
            else:
                raise ValueError("No contentBytes found in the attachment!")

            content_str = extract_text_from_pdf(content_bytes)

        print(content_str)


def extract_text_from_pdf(pdf_bytes):
    """Extracts text from each page of the PDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        full_text += page.get_text()

    return full_text

    # read content of invoice
    # add invoice details to excel file
    # add invoice to google drve
    # move email to folder
