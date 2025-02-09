from langgraph.graph import START, END, StateGraph
from models.state import State
from nodes.append_data_to_table import append_data_to_table
from nodes.extract_structured_data import extract_structured_data
from nodes.read_email_attachments import read_email_attachments
from nodes.download import download
from nodes.other import other
from nodes.meeting import meeting
from nodes.spam import spam
from nodes.classify_email import classify_email
from nodes.extract_email_attachments import extract_email_attachments


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "invoice":
        return "invoice"
    elif state["decision"] == "spam":
        return "spam"
    elif state["decision"] == "meeting":
        return "meeting"
    elif state["decision"] == "download":
        return "download"
    else:
        return "other"


def build_graph() -> StateGraph:

    # Build workflow
    router_builder = StateGraph(State)

    # Add nodes
    router_builder.add_node("classify_email", classify_email)
    router_builder.add_node("extract_email_attachments", extract_email_attachments)
    router_builder.add_node("read_email_attachments", read_email_attachments)
    router_builder.add_node("extract_structured_data", extract_structured_data)
    router_builder.add_node("append_data_to_table", append_data_to_table)
    router_builder.add_node("spam", spam)
    router_builder.add_node("meeting", meeting)
    router_builder.add_node("download", download)
    router_builder.add_node("other", other)

    # Add edges to connect nodes
    router_builder.add_edge(START, "classify_email")
    router_builder.add_conditional_edges(
        "classify_email",
        route_decision,
        {  # Name returned by route_decision : Name of next node to visit
            "invoice": "extract_email_attachments",
            "spam": "spam",
            "meeting": "meeting",
            "download": "download",
            "other": "other",
        },
    )
    router_builder.add_edge("extract_email_attachments", "read_email_attachments")
    router_builder.add_edge("read_email_attachments", "extract_structured_data")
    router_builder.add_edge("extract_structured_data", "append_data_to_table")
    router_builder.add_edge("append_data_to_table", END)
    router_builder.add_edge("spam", END)
    router_builder.add_edge("meeting", END)
    router_builder.add_edge("download", END)
    router_builder.add_edge("other", END)

    # Compile workflow
    graph = router_builder.compile()

    graph_image = graph.get_graph().draw_mermaid_png()
    with open("docs/graph_image.png", "wb") as f:
        f.write(graph_image)

    return graph
