import networkx as nx


def build_distance_two_conflict_graph(radio_graph):
    """
    Build a conflict graph for TDMA scheduling.

    Two nodes conflict if:
    1. They are directly connected (1-hop), OR
    2. They are exactly 2 hops apart / share a common neighbour.
    """

    conflict_graph = nx.Graph()

    # Add all radio nodes
    conflict_graph.add_nodes_from(radio_graph.nodes)

    # Check every pair of nodes
    nodes = list(radio_graph.nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            node_a = nodes[i]
            node_b = nodes[j]

            # Find shortest path between the two nodes
            try:
                distance = nx.shortest_path_length(
                    radio_graph,
                    node_a,
                    node_b
                )
            except nx.NetworkXNoPath:
                continue

            # Distance 1 or 2 means they cannot share a slot
            if distance <= 2:
                conflict_graph.add_edge(node_a, node_b)

    return conflict_graph