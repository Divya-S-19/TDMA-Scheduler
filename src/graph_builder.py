import math
import networkx as nx


RADIO_RANGE = 500.0


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def build_radio_graph(coordinates):
    """
    Create a graph where:
    - each radio is a node
    - an edge exists if two radios are within 500 meters
    """

    graph = nx.Graph()

    # Add all radios as nodes
    for node in coordinates:
        graph.add_node(node)

    # Check every pair of radios
    nodes = list(coordinates.keys())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            node_a = nodes[i]
            node_b = nodes[j]

            distance = calculate_distance(
                coordinates[node_a],
                coordinates[node_b]
            )

            if distance <= RADIO_RANGE:
                graph.add_edge(
                    node_a,
                    node_b,
                    distance=distance
                )

    return graph