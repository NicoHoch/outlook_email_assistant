from models.state import State


def spam(state: State):
    print(state["email"]["sentDateTime"])
    print("Spam email detected!")
