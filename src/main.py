import json
import sys

from .graph_builder import build_radio_graph
from .conflict_graph import build_distance_two_conflict_graph
from .coloring import distance_two_coloring


def load_coordinates():
    """Load node coordinates from the input JSON file."""

    if len(sys.argv) > 1:
        input_path = sys.argv[1]

        try:
            with open(input_path, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"Error: File not found: {input_path}")
            sys.exit(1)

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON file: {input_path}")
            sys.exit(1)

    with open("data/sample_input.json", "r") as file:
        return json.load(file)


def create_schedule_matrix(coloring):
    """Create a Slot × Node binary schedule matrix."""

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
    """Check that no conflicting nodes use the same slot."""

    violations = []

    for node_a, node_b in conflict_graph.edges():

        if coloring[node_a] == coloring[node_b]:
            violations.append(
                (
                    node_a,
                    node_b,
                    coloring[node_a]
                )
            )

    return violations


def main():

    # --------------------------------------------------
    # Load input
    # --------------------------------------------------

    coordinates = load_coordinates()

    # --------------------------------------------------
    # Build radio graph
    # --------------------------------------------------

    radio_graph = build_radio_graph(coordinates)

    print("=" * 60)
    print("TDMA RADIO NETWORK")
    print("=" * 60)

    print(
        f"Total nodes : "
        f"{radio_graph.number_of_nodes()}"
    )

    print(
        f"Total links : "
        f"{radio_graph.number_of_edges()}"
    )

    # --------------------------------------------------
    # Build Distance-2 conflict graph
    # --------------------------------------------------

    conflict_graph = build_distance_two_conflict_graph(
        radio_graph
    )

    print()
    print("=" * 60)
    print("DISTANCE-2 CONFLICT GRAPH")
    print("=" * 60)

    print(
        f"Total conflict pairs : "
        f"{conflict_graph.number_of_edges()}"
    )

    # --------------------------------------------------
    # Color conflict graph
    # --------------------------------------------------

    coloring = distance_two_coloring(
        conflict_graph
    )

    total_slots = max(coloring.values()) + 1

    # --------------------------------------------------
    # Node → Slot assignments
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("TDMA NODE -> SLOT ASSIGNMENTS")
    print("=" * 60)

    for node in sorted(coloring):
        print(
            f"{node}: Slot {coloring[node]}"
        )

    print()
    print(
        f"Total slots used: {total_slots}"
    )

    # --------------------------------------------------
    # Create schedule matrix
    # --------------------------------------------------

    nodes, matrix = create_schedule_matrix(
        coloring
    )

    print()
    print("=" * 60)
    print("TDMA SCHEDULE MATRIX")
    print("=" * 60)

    print("Slot".ljust(8), end="")

    for node in nodes:
        print(node.ljust(10), end="")

    print()

    print("-" * 168)

    for slot, row in enumerate(matrix):

        print(
            str(slot).ljust(8),
            end=""
        )

        for value in row:
            print(
                str(value).ljust(10),
                end=""
            )

        print()

    # --------------------------------------------------
    # Validate schedule
    # --------------------------------------------------

    violations = validate_schedule(
        conflict_graph,
        coloring
    )

    print()
    print("=" * 60)
    print("SCHEDULE VALIDATION")
    print("=" * 60)

    if not violations:

        print("Validation: PASSED")
        print("No Distance-2 conflicts found.")

    else:

        print("Validation: FAILED")

        print(
            f"Number of violations: "
            f"{len(violations)}"
        )

        for node_a, node_b, slot in violations:

            print(
                f"{node_a} <--> {node_b} "
                f"both use Slot {slot}"
            )


if __name__ == "__main__":
    main()