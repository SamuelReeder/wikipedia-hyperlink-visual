"""
We represent hyperlink connections between wikipedia articles with a directed graph.
"""
from __future__ import annotations
from typing import Any, Optional
from api import WikiMediaAPI


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - size: the "length" of this vertex
        - categories: the set of categories this vertex is a part of
        - edges_entering: the vertices that have a directed edge TO this vertex
        - edges_leaving: the vertices that have a directed edge FROM this vertex
    """
    item: Any
    size: int
    categories: set[str]
    edges_entering: list[_Vertex]
    edges_leaving: list[_Vertex]

    def __init__(self, item: any, size: int, categories: set[str], edges_entering: list[_Vertex],
                 edges_leaving: list[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.size = size
        self.categories = categories
        self.edges_entering = edges_entering
        self.edges_leaving = edges_leaving


class DirectedGraph:
    """A graph.

    Private Instance Attributes:
        - _vertices:
            A collection of the vertices contained in this graph.
            Maps item to _Vertex object.
        - _categories:
            A set of the categories to which each element in this
            graph belongs to.
        - _depth:
            The depth to which the graph will expand originating
            from the root article. The depth is defined as the
            maximum length of a connection to the root.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    _vertices: dict[Any, _Vertex]
    _categories: Optional[set[str]]
    _depth: int

    def __init__(self, article: str = None, categories: set[str] = None, depth: int = 10) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self._categories = categories
        self._depth = depth
        if article is not None:
            self.generate_graph(article, self._depth)

    def add_vertex(self, item: Any, size: int, categories: set[str]) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, size, categories, list(), list())

    def add_edge(self, item1: Any, item2: Any) -> None:

        """Add a directed edge going from item1 to item2.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.edges_leaving.append(v2)
            v2.edges_entering.append(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_vertex_keys(self) -> list:
        """
        return the item entries of self._vertices
        """
        return list(self._vertices.keys())

    def get_vertex_values(self) -> list:
        """
        return the values of self._vertice
        """
        return list(self._vertices.values())

    def get_all_edges(self) -> set[tuple[Any, Any]]:
        """Returns all the edges in the directed graph. We will represent each edge by a tuple, where the edge is
        directed from the first entry to the second. The tuple contains vertex items.
        """
        vertices = self._vertices

        edges = set()
        for vertex_item in vertices:
            vertex_object = vertices[vertex_item]
            edges_entering = vertex_object.edges_entering
            edges_leaving = vertex_object.edges_leaving

            for vertex in edges_entering:
                edge = (vertex.item, vertex_item)
                edges.add(edge)

            for vertex in edges_leaving:
                edge = (vertex_item, vertex.item)
                edges.add(edge)

        return edges

    def get_all_categories(self) -> list[set[str]]:
        """Returns all the categories in the DirectedGraph."""
        vertices = self._vertices

        categories = []
        for vertex_item in vertices:
            vertex_object = vertices[vertex_item]
            categories.append(vertex_object.categories)

        return categories

    def get_all_sizes(self) -> list[int]:
        """Returns all the vertex sizes in the DirectedGraph.
        """
        vertices = self._vertices

        sizes = []
        for vertex_item in vertices:
            vertex_object = vertices[vertex_item]
            sizes.append(vertex_object.size)

        return sizes

    def make_graph_from_link_to(self, article: str, articles_link_to: set[str]):
        """
        takes an article and links it to a set of articles that link TO IT. If article is not in the graph, it is added.
        If any article in articles_link_to is not in the graph, they are also added. We make all their sizes 1.
        """

        # First we make the vertices if they do not exist:
        if article not in self.get_vertex_keys():
            self._vertices[article] = _Vertex(article, 1, set(),  list(), list())

        for item in articles_link_to:
            if item not in self.get_vertex_keys():
                self._vertices[item] = _Vertex(item, 1, set(), list(), list())

        # Now we add all edges:
        for item in articles_link_to:
            self._vertices[item].edges_leaving.append(self._vertices[article])
            self._vertices[article].edges_entering.append(self._vertices[item])

    def make_graph_from_link_from(self, article: str, articles_link_from: set[str]):
        """
        takes an article and links it to a set of articles that link FROM IT. If article is not in the graph, it is
        added. If any article in articles_link_from is not in the graph, they are also added. We make all their sizes 1.
        """

        # First we make the vertices if they do not exist:
        if article not in self.get_vertex_keys():
            self._vertices[article] = _Vertex(article, 1, set(), list(), list())

        for item in articles_link_from:
            if item not in self.get_vertex_keys():
                self._vertices[item] = _Vertex(item, 1, set(), list(), list())

        # Now we add all edges:
        for item in articles_link_from:
            self._vertices[item].edges_entering.append(self._vertices[article])
            self._vertices[article].edges_leaving.append(self._vertices[item])

    def generate_graph(self, article: str, depth: int, parent: Any = None) -> None:
        """
        General base method to generate an entire graph
        """
        if depth <= 0 or article in self._vertices:
            return

        properties = WikiMediaAPI.get_article_properties(article)
        if properties is None:
            raise ArticleException('Your article could not be found. Please ensure the title is correct and spaces'
                                   ' are denoted by underscores.')

        if self._categories is not None and self._categories and depth < self._depth:
            if self._categories.intersection(properties['categories']) == set():
                return

        self.add_vertex(properties['name'], properties['size'], properties['categories'])
        if parent is not None:
            self.add_edge(properties['name'], parent)
            self.connect(properties)
        for i in properties['hyperlinks']:
            self.generate_graph(i, depth - 1, properties['name'])

    def connect(self, item_properties: dict) -> None:
        """
        Finds all connections between an article and the existing graph
        """
        for i in self._vertices:
            if i != item_properties['name'] and i in item_properties['hyperlinks']:
                self.add_edge(item_properties['name'], i)


def make_directed_graph_link_to(input_data: list[tuple[str, set[str]]]) -> DirectedGraph:
    """
    makes a directed graph using the input_data, which is a set of tuples. Each tuple contains the name of an article,
    and the set of articles that link TO IT.
    """
    new_graph = DirectedGraph()
    new_graph._categories = set()
    for item in input_data:
        new_graph.make_graph_from_link_to(item[0], item[1])
    return new_graph


def make_directed_graph_link_from(input_data: list[tuple[str, set[str]]]) -> DirectedGraph:
    """
    makes a directed graph using the input_data, which is a set of tuples. Each tuple contains the name of an article,
    and the set of articles that link FROM IT.
    """
    new_graph = DirectedGraph()
    new_graph._categories = set()
    for item in input_data:
        new_graph.make_graph_from_link_from(item[0], item[1])
    return new_graph


class ArticleException(Exception):
    """Exception for when an article can not be found through API
    """
    pass
