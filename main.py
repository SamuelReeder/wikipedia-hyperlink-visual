"""
Main file
"""
from __future__ import annotations
import Grapher
from directedgraph import DirectedGraph
from open_csv import open_csv
import statistics as stat


def csv_graph_test(csv_file: str, colour_by_connectivity: bool) -> None:
    """
    A testing function. It makes a graph based on a CSV file. The file does not contain information regarding size or
    category. Thus, size is set to 1 and category is empty. The node size is proportional to article size.  If color by
     connectivity is false, the nodes are colored by their category. Otherwise, the nodes are colored by how many other
     nodes they are connected to.
    """
    directed_graph = open_csv(csv_file)
    Grapher.visualize_graph(directed_graph, colour_by_connectivity)


def main(article: str, depth: int, colour_by_connectivity: bool, categories: set[str]) -> None:
    """
    The main function. It returns a graph of article and all the articles that connect to up to the given depth. It
    also returns statistics on that graph. The node size is proportional to article size.  If color by
     connectivity is false, the nodes are colored by their category. Otherwise, the nodes are colored by how many other
     nodes they are connected to. "categories" specify a set of 'Category:<category_name>' strings where an article must
     belong to one of these to be included in the graph. In other words, it filters articles by category.

     It also returns the maximally connected node, which is the node which is reached most often when the first
     hyperlink is chosen iteratively.
    """
    directed_graph = DirectedGraph(article, categories, depth)
    Grapher.visualize_graph(directed_graph, colour_by_connectivity)

    # These are all the statistics

    print("The nodes with the maximium number of edges are " + str(stat.node_with_max_edges(directed_graph)))
    print("The nodes with the maximum output to input edges is " + str(stat.node_with_max_output_input(directed_graph)))
    print("The nodes with the maximum input to output edges is " + str(stat.node_with_max_input_output(directed_graph)))


