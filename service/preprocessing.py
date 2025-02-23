from bs4 import BeautifulSoup
import re

import fitz


def clean_text(text):
    # delete spaces and line breaks
    text = re.sub(r"\s+", " ", text)
    # delete special characters
    text = text.replace("\xa0", " ").replace("\r", "").replace("\n", " ")
    # delete specific unwanted characters
    text = re.sub(r"[\u200c\xad͏]", "", text)
    return text.strip()


def get_email_content(email):

    if email["body"]["contentType"] == "html":
        html_body = email["body"]["content"]
        soup = BeautifulSoup(html_body, "lxml")
        raw_text = soup.get_text()
        cleaned_text = clean_text(raw_text)

    else:
        try:
            cleaned_text = clean_text(email["body"]["content"])
        except Exception as e:
            print(f"Fehler beim Dekodieren des E-Mail-Inhalts: {e}")

    return cleaned_text


def extract_text_from_pdf(pdf_bytes):
    """Extracts text from each page of the PDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        full_text += page.get_text()

    return full_text
