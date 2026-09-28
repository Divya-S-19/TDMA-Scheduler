def create_schedule_matrix(coloring):
    """
    Convert Node -> Slot mapping into a Slot x Node matrix.

    1 means the node is scheduled in that slot.
    0 means the node is not scheduled in that slot.
    """

    nodes = sorted(coloring.keys())
    total_slots = max(coloring.values()) + 1

    matrix = []

    for slot in range(total_slots):
        row = []

        for node in nodes:
            if coloring[node] == slot:
                row.append(1)
            else:
                row.append(0)

        matrix.append(row)

    return nodes, matrix


def validate_schedule(conflict_graph, coloring):
    """
    Verify that no two conflicting nodes use the same slot.
    """

    violations = []

    for node_a, node_b in conflict_graph.edges():
        if coloring[node_a] == coloring[node_b]:
            violations.append(
                (node_a, node_b, coloring[node_a])
            )

    return violations