from api.google_vision_ai_api import detect_text_from_image
from models.state import State
import base64

from service.preprocessing import extract_text_from_pdf
import logging


def read_email_attachments(state: State):
    logging.info("Reading email attachments")
    content_str = ""

    attachments = state["attachments"]

    for attachment in attachments:
        mimetype = attachment["contentType"]

        content_base64 = attachment.get("contentBytes")

        if content_base64:
            content_bytes = base64.b64decode(content_base64)
        else:
            raise ValueError("No contentBytes found in the attachment!")
        if mimetype == "image/jpeg" or attachment.get("name", "").endswith(".jpg"):
            content_str += detect_text_from_image(content_bytes)
        # mimetype or attachment.get("name") ends with pdf
        elif mimetype == "application/pdf" or attachment.get("name", "").endswith(
            ".pdf"
        ):
            content_str += extract_text_from_pdf(content_bytes)
        else:
            break

        if len(content_str) > 10000:
            raise ValueError("Content string is too large to process!")

        attachment["contentStr"] = content_str

    return state
