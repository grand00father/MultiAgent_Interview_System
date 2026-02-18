from system.graph.graph_structure import graph_app

def visualization():
    with open("system/graph/graph_picture.jpg", "wb") as f:
        f.write(graph_app.get_graph().draw_mermaid_png())