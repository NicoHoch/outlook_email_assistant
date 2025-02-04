from models.state import State


def other(state: State):
    print(state["email"]["sentDateTime"])
    print("Spam email detected!")
