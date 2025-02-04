from bs4 import BeautifulSoup
import re


def clean_text(text):
    # delete spaces and line breaks
    text = re.sub(r"\s+", " ", text)
    # delete special characters
    text = text.replace("\xa0", " ").replace("\r", "").replace("\n", " ")
    return text.strip()


def get_email_content(msg):
    email_content = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in [
                "text/plain",
                "text/html",
            ]:
                try:
                    payload = part.get_payload(decode=True).decode(
                        part.get_content_charset()
                    )
                    if part.get_content_type() == "text/html":
                        soup = BeautifulSoup(payload, "lxml")
                        raw_text = soup.get_text()
                        email_content = clean_text(raw_text)
                    else:
                        email_content = clean_text(payload)
                    break
                except Exception as e:
                    print(f"Fehler beim Dekodieren des E-Mail-Inhalts: {e}")
    else:
        try:
            email_content = msg.get_payload(decode=True).decode(
                msg.get_content_charset()
            )
        except Exception as e:
            print(f"Fehler beim Dekodieren des E-Mail-Inhalts: {e}")

    return email_content
