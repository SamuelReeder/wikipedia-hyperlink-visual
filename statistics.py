"""
file created to find articles similar to getting to philosophy
"""
from __future__ import annotations
from directedgraph import DirectedGraph, _Vertex
import sys

sys.setrecursionlimit(20000)




def node_with_max_edges(graph: DirectedGraph) -> list:
    """
    returns the node in the graph which has maximum number of edges
    """
    d = {}
    list_of_vertices = []
    for vert in graph.get_vertex_values():
        d[vert] = len(vert.edges_leaving)
    maximum = max(d.values())
    for key in d:
        if d[key] == maximum:
            list_of_vertices += [key.item]
    return list_of_vertices


def node_with_max_output_input(graph: DirectedGraph) -> list:
    """
    returns the node in the graph which has the maximum ratio output edges to input edges
    """
    d = {}
    list_of_vertices = []
    for vert in graph.get_vertex_values():
        if len(vert.edges_entering) != 0:
            d[vert] = len(vert.edges_leaving) / len(vert.edges_entering)
    maximum = max(d.values())
    for key in d:
        if d[key] == maximum:
            list_of_vertices += [key.item]
    return list_of_vertices


def node_with_max_input_output(graph: DirectedGraph) -> list:
    """
    returns the node in the graph which has the maximum ratio of input edges to output edges
    """
    d = {}
    list_of_vertices = []
    for vert in graph.get_vertices2():
        if len(vert.edges_leaving) != 0:
            d[vert] = len(vert.edges_entering) / len(vert.edges_leaving)
    maximum = max(d.values())
    for key in d:
        if d[key] == maximum:
            list_of_vertices += [key.item]
    return list_of_vertices
