from langgraph.graph import START, END, StateGraph
from models.state import State
from nodes.meeting import meeting
from nodes.spam import spam
from nodes.classify_email import classify_email
from nodes.extract_email_attachements import extract_email_attachements


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "invoice":
        return "invoice"
    elif state["decision"] == "spam":
        return "spam"
    elif state["decision"] == "meeting":
        return "meeting"


def build_graph() -> StateGraph:

    # Build workflow
    router_builder = StateGraph(State)

    # Add nodes
    router_builder.add_node("extract_email_attachements", extract_email_attachements)
    router_builder.add_node("spam", spam)
    router_builder.add_node("meeting", meeting)
    router_builder.add_node("classify_email", classify_email)

    # Add edges to connect nodes
    router_builder.add_edge(START, "classify_email")
    router_builder.add_conditional_edges(
        "classify_email",
        route_decision,
        {  # Name returned by route_decision : Name of next node to visit
            "invoice": "extract_email_attachements",
            "spam": "spam",
            "meeting": "meeting",
        },
    )
    router_builder.add_edge("extract_email_attachements", END)
    router_builder.add_edge("spam", END)
    router_builder.add_edge("meeting", END)

    # Compile workflow
    graph = router_builder.compile()

    graph_image = graph.get_graph().draw_mermaid_png()
    with open("docs/graph_image.png", "wb") as f:
        f.write(graph_image)

    return graph
