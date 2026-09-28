import networkx as nx


def greedy_color_with_order(graph, order):
    """
    Greedily color the graph using a given node ordering.

    Each color represents one TDMA slot.
    """

    coloring = {}

    for node in order:

        used_slots = {
            coloring[neighbor]
            for neighbor in graph.neighbors(node)
            if neighbor in coloring
        }

        slot = 0

        while slot in used_slots:
            slot += 1

        coloring[node] = slot

    return coloring


def number_of_slots(coloring):
    """Return the number of TDMA slots used."""

    if not coloring:
        return 0

    return max(coloring.values()) + 1


def distance_two_coloring(conflict_graph):
    """
    Try multiple greedy coloring strategies and return
    the coloring that uses the fewest TDMA slots.

    Distance-2 conflicts are already represented as edges
    in the conflict graph.
    """

    nodes = list(conflict_graph.nodes)

    candidate_orders = []

    # --------------------------------------------------
    # Strategy 1: Highest degree first
    # --------------------------------------------------

    degree_order = sorted(
        nodes,
        key=lambda node: (
            conflict_graph.degree[node],
            node
        ),
        reverse=True
    )

    candidate_orders.append(degree_order)

    # --------------------------------------------------
    # Strategy 2: Lowest degree first
    # --------------------------------------------------

    low_degree_order = sorted(
        nodes,
        key=lambda node: (
            conflict_graph.degree[node],
            node
        )
    )

    candidate_orders.append(low_degree_order)

    # --------------------------------------------------
    # Strategy 3: DSATUR ordering
    # --------------------------------------------------

    dsatur_order = []

    temporary_coloring = {}

    while len(dsatur_order) < len(nodes):

        uncolored = [
            node
            for node in nodes
            if node not in temporary_coloring
        ]

        def saturation(node):

            neighbor_colors = {
                temporary_coloring[neighbor]
                for neighbor in conflict_graph.neighbors(node)
                if neighbor in temporary_coloring
            }

            return len(neighbor_colors)

        selected = max(
            uncolored,
            key=lambda node: (
                saturation(node),
                conflict_graph.degree[node],
                node
            )
        )

        used_colors = {
            temporary_coloring[neighbor]
            for neighbor in conflict_graph.neighbors(selected)
            if neighbor in temporary_coloring
        }

        color = 0

        while color in used_colors:
            color += 1

        temporary_coloring[selected] = color
        dsatur_order.append(selected)

    candidate_orders.append(dsatur_order)

    # --------------------------------------------------
    # Strategy 4: NetworkX greedy strategy
    # --------------------------------------------------

    nx_order = list(
        nx.greedy_color(
            conflict_graph,
            strategy="largest_first"
        ).keys()
    )

    candidate_orders.append(nx_order)

    # --------------------------------------------------
    # Evaluate all candidates
    # --------------------------------------------------

    best_coloring = None
    best_slot_count = float("inf")

    for order in candidate_orders:

        coloring = greedy_color_with_order(
            conflict_graph,
            order
        )

        slots = number_of_slots(coloring)

        if slots < best_slot_count:
            best_slot_count = slots
            best_coloring = coloring

    print(
        f"\nColoring optimization: "
        f"{best_slot_count} slots selected."
    )

    return best_coloring