\# TDMA Schedule Planner and Optimizer



\## 1. Project Overview



This project implements a centralized Schedule Planner and Optimizer for a TDMA wireless network.



The system takes static coordinates of wireless radios, builds the communication and conflict relationships, and generates a conflict-free TDMA schedule.



The implementation is divided into:



\- Part 1: TDMA schedule generation using distance-2 graph coloring

\- Part 2: EMANE integration approach and schedule adapter prototype



\---



\## 2. Problem Statement



The objective is to create a centralized software brain that calculates a TDMA schedule for wireless nodes.



Two nodes must not transmit in the same time slot when:



1\. They are directly connected, or

2\. They share a common neighboring node.



Nodes sufficiently far apart can reuse the same time slot.



The scheduler therefore models the wireless network as a graph and solves the resulting distance-2 coloring problem using heuristic graph-coloring techniques.



\---



\## 3. Input



The scheduler accepts node coordinates in JSON format.



Example:



{

&#x20;   "Node\_01": \[0, 0],

&#x20;   "Node\_02": \[300, 0],

&#x20;   "Node\_03": \[600, 0],

&#x20;   "Node\_04": \[900, 0],

&#x20;   "Node\_05": \[0, 300],

&#x20;   "Node\_06": \[300, 300],

&#x20;   "Node\_07": \[600, 300],

&#x20;   "Node\_08": \[900, 300],

&#x20;   "Node\_09": \[0, 600],

&#x20;   "Node\_10": \[300, 600],

&#x20;   "Node\_11": \[600, 600],

&#x20;   "Node\_12": \[900, 600],

&#x20;   "Node\_13": \[0, 900],

&#x20;   "Node\_14": \[300, 900],

&#x20;   "Node\_15": \[600, 900],

&#x20;   "Node\_16": \[900, 900]

}



The radio communication range is 500 meters.



\---



\## 4. Design Process



The implementation follows this pipeline:



Coordinates

&#x20;   ↓

Radio Graph

&#x20;   ↓

Distance-2 Conflict Graph

&#x20;   ↓

Graph Coloring

&#x20;   ↓

Schedule Validation

&#x20;   ↓

Slot × Node Matrix



\### 4.1 Radio Graph



Each radio is represented as a graph node.



An edge is created between two radios when their Euclidean distance is less than or equal to 500 meters.



\### 4.2 Distance-2 Conflict Graph



A second graph is constructed for scheduling.



Two nodes are connected in this graph when their shortest-path distance in the radio graph is at most two.



Therefore, the conflict graph represents both:



\- Direct interference relationships

\- Two-hop/common-neighbor conflicts



\### 4.3 Coloring



Each graph color represents a TDMA time slot.



The scheduler uses several greedy ordering strategies and selects the coloring requiring the fewest slots among the generated candidates.



The strategies include:



\- Highest-degree ordering

\- Lowest-degree ordering

\- DSATUR-style ordering

\- NetworkX largest-first ordering



\### 4.4 Validation



After coloring, every conflict edge is checked.



If two conflicting nodes have the same slot, the schedule is rejected as invalid.



A valid schedule contains no distance-2 conflicts.



\---



\## 5. Final Part 1 Results



For the provided 16-node sample topology:



\- Total nodes: 16

\- Total radio links: 42

\- Total conflict pairs: 90

\- Total slots used: 9

\- Schedule validation: PASSED

\- Distance-2 conflicts: None



The exact coloring verifier was also used to check the minimum number of slots for this specific sample.



It established that:



\- 1 to 8 slots: Not possible

\- 9 slots: Possible



Therefore, 9 slots is the minimum for this particular sample topology.



\---



\## 6. Final Node-to-Slot Mapping



Node\_01 → Slot 8

Node\_02 → Slot 5

Node\_03 → Slot 4

Node\_04 → Slot 8

Node\_05 → Slot 7

Node\_06 → Slot 3

Node\_07 → Slot 2

Node\_08 → Slot 7

Node\_09 → Slot 6

Node\_10 → Slot 1

Node\_11 → Slot 0

Node\_12 → Slot 6

Node\_13 → Slot 8

Node\_14 → Slot 5

Node\_15 → Slot 4

Node\_16 → Slot 8



\---



\## 7. Schedule Matrix



| Slot | Active Nodes |

|------|--------------|

| 0 | Node\_11 |

| 1 | Node\_10 |

| 2 | Node\_07 |

| 3 | Node\_06 |

| 4 | Node\_03, Node\_15 |

| 5 | Node\_02, Node\_14 |

| 6 | Node\_09, Node\_12 |

| 7 | Node\_05, Node\_08 |

| 8 | Node\_01, Node\_04, Node\_13, Node\_16 |



The matrix can also be represented as a binary Slot × Node matrix where:



\- `1` means the node is scheduled in that slot

\- `0` means the node is not scheduled in that slot



\---



\## 8. Exact Verification



Because graph coloring is computationally difficult in general, a separate exact backtracking verifier was implemented for the 16-node sample.



The verifier checks whether the conflict graph can be colored with a specified number of slots.



For the sample topology:



8 slots → Not possible

9 slots → Possible



This provides an exact verification for the sample input while the main scheduler remains heuristic-based.



\---



\## 9. Testing



Automated tests were implemented using pytest.



The test suite verifies:



\- Radio graph construction

\- Distance-2 conflict detection

\- Schedule validity

\- Schedule matrix generation



Final test result:



4 passed



\---



\# Part 2 — EMANE Integration Approach



\## 10. Objective



Part 2 extends the scheduling system toward an EMANE-based TDMA simulation.



The intended architecture is:



Python Scheduler

&#x20;   ↓

Node-to-Slot Schedule

&#x20;   ↓

Schedule Adapter

&#x20;   ↓

EMANE TDMA Schedule Event

&#x20;   ↓

EMANE TDMA Radio Model

&#x20;   ↓

Scheduled Packet Transmission



\---



\## 11. Schedule Adapter



A Python adapter was implemented in:



part2\_emane/schedule\_adapter.py



The adapter reads the generated Node-to-Slot mapping and converts it into a generic XML representation.



The prototype includes:



\- Node identifier

\- Assigned slot

\- Slot duration



The current prototype uses a slot duration of 1 ms.



\---



\## 12. Generated Schedule



The adapter successfully generated:



part2\_emane/generated\_schedule.xml



The generated XML contains all 16 node assignments.



Example structure:



<tdma\_schedule slot\_duration\_ms="1">

&#x20;   <assignment node="Node\_01" slot="8" />

&#x20;   ...

</tdma\_schedule>



This demonstrates the conversion from the Python scheduling output into a format suitable for a later EMANE integration layer.



\---



\## 13. EMANE Integration Plan



The planned integration consists of:



1\. Install and configure EMANE in a suitable Linux environment.

2\. Configure the EMANE TDMA Radio Model.

3\. Configure the required slot duration, frame structure and frequencies.

4\. Connect the Python-generated schedule to the EMANE TDMA scheduling mechanism.

5\. Apply the schedule to the simulation.

6\. Generate traffic between nodes.

7\. Verify that transmissions follow the calculated TDMA schedule.



The exact event/XML/ProtoBuf schema must match the EMANE version and TDMA model used in the target environment.



\---



\## 14. Current Part 2 Status



Completed:



\- Part 2 architecture

\- Schedule adapter prototype

\- Sample schedule input

\- Generic XML schedule generation



Not claimed as completed:



\- Actual EMANE installation

\- Actual EMANE TDMA event injection

\- Packet-level EMANE simulation



The current implementation therefore demonstrates the integration approach without claiming successful packet-level EMANE execution.



\---



\## 15. Project Structure



TDMA-Scheduler/



├── src/

│   ├── main.py

│   ├── graph\_builder.py

│   ├── conflict\_graph.py

│   ├── coloring.py

│   ├── scheduler.py

│   ├── exact\_coloring.py

│   └── verify\_optimum.py

│

├── data/

│   └── sample\_input.json

│

├── tests/

│   └── test\_scheduler.py

│

├── part2\_emane/

│   ├── README.md

│   ├── schedule\_adapter.py

│   ├── sample\_schedule.json

│   └── generated\_schedule.xml

│

├── documentation/

├── presentation/

├── requirements.txt

└── README.md



\---



\## 16. Technologies Used



\- Python

\- NetworkX

\- Pytest

\- XML processing

\- Graph theory

\- Greedy graph coloring

\- DSATUR-style scheduling

\- Backtracking-based exact verification

\- EMANE integration approach



\---



\## 17. Limitations



The main scheduler uses heuristic graph coloring for practical scheduling.



The heuristic does not guarantee a globally minimum coloring for arbitrary input topologies.



The exact verifier provides minimum-slot verification for the sample topology but is not intended as the primary scheduler for large networks because exact graph coloring can become computationally expensive.



The Part 2 XML is an integration prototype and is not claimed to be an official EMANE event schema.



\---



\## 18. Conclusion



The project successfully implements the mandatory centralized TDMA scheduling component.



For the supplied 16-node topology, the scheduler generates a conflict-free schedule using 9 slots.



The result was validated using both:



\- Conflict checking

\- Exact coloring verification



A Part 2 EMANE integration architecture and schedule adapter prototype were also implemented to demonstrate how the Python-generated schedule can be connected to an EMANE TDMA simulation environment.

