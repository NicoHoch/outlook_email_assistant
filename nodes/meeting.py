from models.state import State


def meeting(state: State):
    print(state["email"]["sentDateTime"])
    print("Meeting email detected!")
