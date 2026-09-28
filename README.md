# TDMA Scheduler – Network Brain

A Python-based TDMA scheduling system for a wireless radio network.

The system models radios as graph nodes, creates communication links based on distance, builds a Distance-2 conflict graph, and assigns TDMA time slots using graph coloring.

## Problem

In a TDMA wireless network, multiple radios share the same frequency by transmitting in different time slots.

Two radios should not transmit in the same slot when:

- They are directly connected (1-hop), or
- They are separated by two hops and therefore share a common neighbour.

Radios separated by more than two hops can reuse the same slot.

This project implements the scheduling logic using graph theory.

## Features

- Reads radio coordinates from a JSON file
- Builds a wireless radio graph
- Uses a 500-meter communication range
- Builds a Distance-2 conflict graph
- Applies greedy graph-coloring strategies
- Selects the coloring using the fewest slots among the tested strategies
- Generates a Node-to-Slot mapping
- Generates a Slot × Node binary schedule matrix
- Validates the schedule for Distance-2 conflicts
- Includes automated tests
- Includes an exact coloring verifier for the small sample network

## Project Structure

```text
TDMA-Scheduler/
│
├── src/
│   ├── main.py
│   ├── graph_builder.py
│   ├── conflict_graph.py
│   ├── coloring.py
│   ├── scheduler.py
│   ├── exact_coloring.py
│   └── verify_optimum.py
│
├── data/
│   └── sample_input.json
│
├── tests/
│   └── test_scheduler.py
│
├── part2_emane/
│
├── documentation/
│
├── presentation/
│
├── venv/
│
└── requirements.txt