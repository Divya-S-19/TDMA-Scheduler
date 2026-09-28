def can_color_with_k(graph, k):
    """
    Check whether the graph can be colored using at most k colors.
    Uses backtracking with the most-constrained node selection.
    """

    nodes = list(graph.nodes)
    coloring = {}

    def select_node():
        uncolored = [
            node for node in nodes
            if node not in coloring
        ]

        return max(
            uncolored,
            key=lambda node: (
                len({
                    coloring[n]
                    for n in graph.neighbors(node)
                    if n in coloring
                }),
                graph.degree[node]
            )
        )

    def backtrack():

        if len(coloring) == len(nodes):
            return True

        node = select_node()

        used_colors = {
            coloring[neighbor]
            for neighbor in graph.neighbors(node)
            if neighbor in coloring
        }

        for color in range(k):

            if color in used_colors:
                continue

            coloring[node] = color

            if backtrack():
                return True

            del coloring[node]

        return False

    if backtrack():
        return True, coloring.copy()

    return False, None