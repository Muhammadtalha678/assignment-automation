from graphviz import Digraph
import os

# diag = {
    
#                     "title": "Challenge of Status Quo by Critical Thinkers",
#                     "diagram_type": "process_diagram",
#                     "layout": "TB",
#                     "nodes": [
#                         "Identify Norms",
#                         "Question Beliefs",
#                         "Gather Evidence",
#                         "Analyze Perspectives",
#                         "Propose Changes",
#                         "Influence Society"
#                     ],
#                     "connections": [
#                         [
#                             "Identify Norms",
#                             "Question Beliefs"
#                         ],
#                         [
#                             "Question Beliefs",
#                             "Gather Evidence"
#                         ],
#                         [
#                             "Gather Evidence",
#                             "Analyze Perspectives"
#                         ],
#                         [
#                             "Analyze Perspectives",
#                             "Propose Changes"
#                         ],
#                         [
#                             "Propose Changes",
#                             "Influence Society"
#                         ]
#                     ]
# }
def generate_graphviz_diagram(idx:int, diagram: dict , output_dir="diagrams"):
    """
    Generate Graphviz diagram from LLM output.

    Parameters
    ----------
    diagram : dict
        {
            "title": "...",
            "diagram_type": "...",
            "layout": "TB",
            "nodes": [...],
            "connections": [[from,to],...]
        }

    Returns
    -------
    str
        PNG file path
    """

    os.makedirs(output_dir, exist_ok=True)
    print(diagram["title"])
    graph = Digraph(
        name=diagram["title"],
        format="png"
    )

    graph.attr(rankdir=diagram.get("layout", "TB"))

    graph.attr(
        bgcolor="white",
        dpi="300"
    )

    graph.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="#EAF3FF",
        color="#2F5597",
        fontname="Arial",
        fontsize="12",
        margin="0.2"
    )

    graph.attr(
        "edge",
        color="black",
        arrowsize="0.8"
    )

    for node in diagram["nodes"]:
        graph.node(node)

    for source, target in diagram["connections"]:
        graph.edge(source, target)

    filename = os.path.join(
        output_dir,
        f"temp_{idx}"
    )

    graph.render(filename, cleanup=True)

    return filename + ".png"    
