from langgraph.graph import START, END, StateGraph
from models.state import State
from nodes.classify_email import classify_email
from nodes.extract_email_attachements import extract_email_attachements
from IPython.display import Image, display


def build_graph() -> StateGraph:
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node(classify_email)
    graph_builder.add_node(extract_email_attachements)

    # Add edges
    graph_builder.add_edge(START, "classify_email")
    graph_builder.add_edge("classify_email", "extract_email_attachements")
    graph_builder.add_edge("extract_email_attachements", END)

    graph = graph_builder.compile()

    graph_image = graph.get_graph().draw_mermaid_png()
    with open("docs/graph_image.png", "wb") as f:
        f.write(graph_image)

    return graph
