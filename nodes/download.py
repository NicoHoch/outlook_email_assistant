from models.state import State


def download(state: State):
    print(state["email"]["sentDateTime"])
    print("Spam email detected!")
