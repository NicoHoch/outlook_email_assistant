from langgraph.graph import START, END, StateGraph
from models.state import State
from nodes.append_data_to_table import append_data_to_table
from nodes.extract_structured_data import extract_structured_data
from nodes.read_email_attachments import read_email_attachments
from nodes.download import download
from nodes.other import other
from nodes.meeting import meeting
from nodes.classify_email import classify_email
from nodes.extract_email_attachments import extract_email_attachments
from nodes.upload_file_to_drive import upload_file_to_drive
from nodes.mark_email_as_read import mark_email_as_read
from nodes.move_email_to_spam import move_email_to_spam
import os


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "invoice":
        return "invoice"
    elif state["decision"] == "advertisement":
        return "advertisement"
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
    router_builder.add_node("save_invoice_to_drive", upload_file_to_drive)
    router_builder.add_node("mark_email_as_read", mark_email_as_read)
    router_builder.add_node("move_email_to_spam", move_email_to_spam)
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
            "advertisement": "move_email_to_spam",
            "meeting": "meeting",
            "download": "download",
            "other": "other",
        },
    )
    router_builder.add_edge("extract_email_attachments", "read_email_attachments")
    router_builder.add_edge("read_email_attachments", "extract_structured_data")
    router_builder.add_edge("extract_structured_data", "save_invoice_to_drive")
    router_builder.add_edge("save_invoice_to_drive", "append_data_to_table")
    router_builder.add_edge("append_data_to_table", "mark_email_as_read")
    router_builder.add_edge("move_email_to_spam", "mark_email_as_read")
    router_builder.add_edge("mark_email_as_read", END)
    router_builder.add_edge("meeting", END)
    router_builder.add_edge("download", END)
    router_builder.add_edge("other", END)

    # Compile workflow
    graph = router_builder.compile()

    if os.getenv("ENV") == "dev":
        graph_image = graph.get_graph().draw_mermaid_png()
        with open("docs/graph_image.png", "wb") as f:
            f.write(graph_image)

    return graph
