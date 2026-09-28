import json

from graph_builder import build_radio_graph
from conflict_graph import build_distance_two_conflict_graph
from exact_coloring import can_color_with_k


def main():

    with open("data/sample_input.json", "r") as file:
        coordinates = json.load(file)

    radio_graph = build_radio_graph(coordinates)

    conflict_graph = build_distance_two_conflict_graph(
        radio_graph
    )

    print("=" * 60)
    print("EXACT COLORING VERIFICATION")
    print("=" * 60)

    for k in range(1, len(conflict_graph.nodes) + 1):

        print(f"Testing {k} slots...", end=" ")

        possible, coloring = can_color_with_k(
            conflict_graph,
            k
        )

        if possible:

            print("POSSIBLE")

            print("\nMinimum slots for this sample:", k)

            print("\nNode -> Slot")

            for node in sorted(coloring):
                print(
                    f"{node}: Slot {coloring[node]}"
                )

            break

        else:
            print("NOT POSSIBLE")


if __name__ == "__main__":
    main()