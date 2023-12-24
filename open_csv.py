"""
Converts a csv file into a directed graph. The first entry in a row is an article, and the rest of the entries in that
row are the articles that link TO IT.
"""

import csv
from directedgraph import make_directed_graph_link_to, DirectedGraph


def open_csv(csv_file: str) -> DirectedGraph:
    """Takes a csv file and converts it into a directed graph
    """
    with open(csv_file, "r", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",")

        data = list()
        for row in reader:
            article = row[0]
            link_to = set(row[1:])
            data.append((article, link_to))

        return make_directed_graph_link_to(data)
