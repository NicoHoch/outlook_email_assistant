from models.state import State


def classify_email(state: State):
    print(state["email"]["subject"])
