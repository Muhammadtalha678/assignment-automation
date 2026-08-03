from graphviz import Digraph
import os

# # diag = {
    
# #                     "title": "Challenge of Status Quo by Critical Thinkers",
# #                     "diagram_type": "process_diagram",
# #                     "layout": "TB",
# #                     "nodes": [
# #                         "Identify Norms",
# #                         "Question Beliefs",
# #                         "Gather Evidence",
# #                         "Analyze Perspectives",
# #                         "Propose Changes",
# #                         "Influence Society"
# #                     ],
# #                     "connections": [
# #                         [
# #                             "Identify Norms",
# #                             "Question Beliefs"
# #                         ],
# #                         [
# #                             "Question Beliefs",
# #                             "Gather Evidence"
# #                         ],
# #                         [
# #                             "Gather Evidence",
# #                             "Analyze Perspectives"
# #                         ],
# #                         [
# #                             "Analyze Perspectives",
# #                             "Propose Changes"
# #                         ],
# #                         [
# #                             "Propose Changes",
# #                             "Influence Society"
# #                         ]
# #                     ]
# # }
# def generate_graphviz_diagram(idx:int, diagram: dict , output_dir="diagrams"):
#     """
#     Generate Graphviz diagram from LLM output.

#     Parameters
#     ----------
#     diagram : dict
#         {
#             "title": "...",
#             "diagram_type": "...",
#             "layout": "TB",
#             "nodes": [...],
#             "connections": [[from,to],...]
#         }

#     Returns
#     -------
#     str
#         PNG file path
#     """

#     os.makedirs(output_dir, exist_ok=True)
#     print(diagram["title"])
#     graph = Digraph(
#         name=diagram["title"],
#         format="png"
#     )

#     # graph.attr(rankdir=diagram.get("layout", "TB"))

#     # # graph.attr(
#     # #     bgcolor="white",
#     # #     dpi="300"
#     # # )
#     # graph.attr(
#     #     bgcolor="white",
#     #     dpi="300",
#     #     splines="ortho",
#     #     ranksep="0.7",
#     #     nodesep="0.45",
#     #     pad="0.3"
#     #     )

#     # # graph.attr(
#     # #     "node",
#     # #     shape="box",
#     # #     style="rounded,filled",
#     # #     fillcolor="#EAF3FF",
#     # #     color="#2F5597",
#     # #     fontname="Arial",
#     # #     fontsize="12",
#     # #     margin="0.2"
#     # # )
#     # graph.attr(
#     #     "node",
#     #     shape="box",
#     #     style="rounded,filled",
#     #     fillcolor="white",
#     #     color="black",
#     #     penwidth="1.5",
#     #     fontname="Calibri",
#     #     fontsize="11",
#     #     margin="0.18"
#     #    )
#     # # graph.attr(
#     # #     "edge",
#     # #     color="black",
#     # #     arrowsize="0.8"
#     # # )
#     # graph.attr(
#     #     "edge",
#     #     color="black",
#     #     penwidth="1.2",
#     #     arrowsize="0.7"
#     #     )

#     # 1. High DPI for crisp rendering (No Blur)
#     graph.attr(
#         bgcolor="white",
#         dpi="300",         # Crisp high quality render
#         rankdir=diagram.get("layout", "TB"),
#         splines="ortho",
#         ranksep="1.0",     # Nodes ke darmayan fasla barhaya (Pehle 0.7 tha)
#         nodesep="0.8",     # Horizontal distance barhaya (Pehle 0.45 tha)
#         pad="0.5"          # Margin around image
#     )

#     # 2. Dynamic Node Width and Auto-wrapping
#     # Shape, Font size aur Margin improve kia
#     graph.attr(
#         "node",
#         shape="box",
#         style="rounded,filled",
#         fillcolor="#F8FAFC",  # Soft white/grey background
#         color="#1E293B",      # Dark border
#         penwidth="1.8",
#         fontname="Arial",
#         fontsize="12",        # Visible text
#         margin="0.3,0.2"      # Internal padding for text breathing room
#     )

#     graph.attr(
#         "edge",
#         color="#334155",
#         penwidth="1.5",
#         arrowsize="0.9"
#     )

#     for node in diagram["nodes"]:
#         graph.node(node)

#     for source, target in diagram["connections"]:
#         graph.edge(source, target)

#     filename = os.path.join(
#         output_dir,
#         f"temp_{idx}"
#     )

#     graph.render(filename, cleanup=True)

#     return filename + ".png"    


# graphviz_diagram.py

def generate_graphviz_diagram(idx: int, diagram: dict, output_dir="diagrams"):
    os.makedirs(output_dir, exist_ok=True)
    
    graph = Digraph(
        name=diagram["title"],
        format="png"
    )

    # Force Horizontal Layout & Compact Margins
    graph.attr(
        bgcolor="white",
        dpi="300",
        rankdir="LR",        # Force Left-to-Right flow
        splines="ortho",
        ranksep="0.5",       # Reduced gap between ranks (Pehle 1.0 tha)
        nodesep="0.4",       # Reduced gap between nodes
        pad="0.1"            # Minimal padding around graph border (Pehle empty border bari thi)
    )

    graph.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="#F8FAFC",
        color="#1E293B",
        penwidth="1.5",
        fontname="Arial",
        fontsize="11",
        margin="0.2,0.1"     # Tight internal node padding
    )

    graph.attr(
        "edge",
        color="#334155",
        penwidth="1.2",
        arrowsize="0.8"
    )

    for node in diagram["nodes"]:
        graph.node(node)

    for source, target in diagram["connections"]:
        graph.edge(source, target)

    filename = os.path.join(output_dir, f"temp_{idx}")
    graph.render(filename, cleanup=True)

    return filename + ".png"

# def generate_graphviz_diagram(idx: int, diagram: dict, output_dir="diagrams"):
#     os.makedirs(output_dir, exist_ok=True)
    
#     graph = Digraph(
#         name=diagram["title"],
#         format="png"
#     )

#     # Second PDF style (Vertical Layout with Compact Spacing)
#     graph.attr(
#         bgcolor="white",
#         dpi="300",
#         rankdir="TB",        # ✅ Second PDF jesa vertical flow
#         splines="ortho",
#         ranksep="0.4",       # Nodes ke darmayan kam vertical space (Compact Look)
#         nodesep="0.3",       # Horizontal space control
#         pad="0.1"            # Borders tight rakhne ke liye
#     )

#     graph.attr(
#         "node",
#         shape="box",
#         style="rounded,filled",
#         fillcolor="white",   # ✅ Second PDF ki tarah clean white fill
#         color="black",       # Black borders
#         penwidth="1.2",
#         fontname="Arial",
#         fontsize="10",       # Clean visible text
#         margin="0.15,0.08"   # Node padding tight rakhein
#     )

#     graph.attr(
#         "edge",
#         color="black",
#         penwidth="1.2",
#         arrowsize="0.7"
#     )

#     for node in diagram["nodes"]:
#         graph.node(node)

#     for source, target in diagram["connections"]:
#         graph.edge(source, target)

#     filename = os.path.join(output_dir, f"temp_{idx}")
#     graph.render(filename, cleanup=True)

#     return filename + ".png"