import json
from api import notion_api
from api.openai_api import OpenAIClient
from models.state import State
import logging


def add_lead_to_crm(state: State) -> dict:

    email_subject = state["email"]["subject"]
    email_category = state["category"]

    try:
        name = email_subject.split("Neues Ereignis: ")[1].split(" -")[0]
    except IndexError:
        logging.error("Failed to extract email event from subject")
        name = "Unknown Name"

    company = "Unknown Company"
    notion_api.add_lead_to_crm(name, company, email_category, email_subject)

    return state
