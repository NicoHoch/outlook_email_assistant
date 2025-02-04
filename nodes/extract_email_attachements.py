from models.state import State


def extract_email_attachements(state: State):
    print(state["email"]["sentDateTime"])
