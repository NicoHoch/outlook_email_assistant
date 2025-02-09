from api.google_vision_ai_api import detect_text_from_image
from models.state import State
import base64

from service.preprocessing import extract_text_from_pdf  # PyMuPDF


def read_email_attachments(state: State):

    attachments = state["attachments"]

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

        # Add content_str to the attachment
        attachment["contentStr"] = content_str

    return state
