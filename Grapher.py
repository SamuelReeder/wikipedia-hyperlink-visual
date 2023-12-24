"""
This allows us to graph
"""

from __future__ import annotations
from directedgraph import DirectedGraph
import plotly.graph_objects as go
import networkx as nx
from open_csv import open_csv
import sys



def normalize_and_scale(vertex_sizes: list[int], min_size: int = 10, max_size: int = 50):
    """
    Normalizes and scales the sizes of each vertex to optimize for the graph
    """
    min_raw_size = min(vertex_sizes)
    max_raw_size = max(vertex_sizes)
    divisor = max_raw_size - min_raw_size
    if divisor == 0:
        divisor = max_raw_size

    new = []
    for i in vertex_sizes:
        normalized_size = (i - min_raw_size) / divisor
        new.append(normalized_size * (max_size - min_size) + min_size)

    return new


def visualize_graph(graph: DirectedGraph, colour_by_connectivity: bool = True) -> None:
    """A visualization of a directed graph using plotly and networkx. The edges are uniform (their direction is not
    shown)
    """
    network_graph = nx.Graph()

    vertices = list(graph.get_vertex_keys())
    network_graph.add_nodes_from(vertices)

    edges = graph.get_all_edges()
    network_graph.add_edges_from(edges)
    pos = nx.spring_layout(network_graph, k=0.15)

    edge_x = []
    edge_y = []
    for edge in network_graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    x = [pos[node][0] for node in network_graph.nodes()]
    y = [pos[node][1] for node in network_graph.nodes()]

    vertex_sizes = normalize_and_scale(graph.get_all_sizes())
    vertex_edges = [len(list(network_graph.neighbors(n))) for n in vertices]
    vertex_categories = [len(i) for i in graph.get_all_categories()]

    vertex_trace = go.Scatter(
        x=x, y=y,
        mode='markers',
        hoverinfo='text',
        hovertext=vertices,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            reversescale=True,
            color=vertex_edges if colour_by_connectivity else vertex_categories,
            size=vertex_sizes,
            sizemode='diameter',
            line_width=2,
            colorbar=dict(
                thickness=15,
                title='Vertex Connections' if colour_by_connectivity else 'Number of Categories',
                xanchor='left',
                titleside='right'
            ),
        )
    )

    layout = go.Layout(
        title='Wikipedia Hyperlink Connectivity Visualization',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    fig = go.Figure(data=[edge_trace, vertex_trace], layout=layout)
    fig.show()
