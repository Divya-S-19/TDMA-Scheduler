import sys
from pathlib import Path

# Allow Python to find the files inside src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from graph_builder import build_radio_graph
from conflict_graph import build_distance_two_conflict_graph
from coloring import distance_two_coloring
from scheduler import create_schedule_matrix, validate_schedule


def test_radio_graph():
    coordinates = {
        "A": [0, 0],
        "B": [300, 0],
        "C": [600, 0]
    }

    graph = build_radio_graph(coordinates)

    assert graph.number_of_nodes() == 3
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "C")
    assert not graph.has_edge("A", "C")


def test_distance_two_conflict():
    coordinates = {
        "A": [0, 0],
        "B": [300, 0],
        "C": [600, 0]
    }

    radio_graph = build_radio_graph(coordinates)
    conflict_graph = build_distance_two_conflict_graph(radio_graph)

    # A and C are two hops apart, so they must conflict.
    assert conflict_graph.has_edge("A", "C")


def test_schedule_is_valid():
    coordinates = {
        "A": [0, 0],
        "B": [300, 0],
        "C": [600, 0]
    }

    radio_graph = build_radio_graph(coordinates)
    conflict_graph = build_distance_two_conflict_graph(radio_graph)

    coloring = distance_two_coloring(conflict_graph)

    violations = validate_schedule(
        conflict_graph,
        coloring
    )

    assert violations == []


def test_schedule_matrix():
    coloring = {
        "A": 0,
        "B": 1,
        "C": 0
    }

    nodes, matrix = create_schedule_matrix(coloring)

    assert nodes == ["A", "B", "C"]
    assert matrix == [
        [1, 0, 1],
        [0, 1, 0]
    ]