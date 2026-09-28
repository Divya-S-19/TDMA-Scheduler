\# TDMA Schedule Planner and Optimizer



\## Slide 1 — Title



\### TDMA Schedule Planner and Optimizer



Centralized Schedule Planning for a Wireless TDMA Network



\*\*Technology:\*\* Python + NetworkX



\*\*Project:\*\* Wireless Protocol Development



\---



\## Slide 2 — Problem Statement



\### Objective



Develop a centralized scheduler that calculates conflict-free TDMA transmission slots for wireless nodes.



\### Key Constraint



Two nodes cannot use the same slot when:



\- They are directly connected, or

\- They are within two hops / share a common neighbour.



Nodes beyond the two-hop conflict relationship can reuse slots.



\---



\## Slide 3 — Input and Network Model



\### Input



16 wireless nodes with static `(x, y)` coordinates.



\### Radio Range



500 meters.



\### Processing



Coordinates

↓

Radio Graph

↓

Distance-2 Conflict Graph

↓

Graph Coloring

↓

TDMA Schedule



The radio graph represents communication relationships.



The conflict graph represents scheduling restrictions.



\---



\## Slide 4 — Distance-2 Conflict Graph



\### Why Distance-2?



A direct neighbour creates a transmission conflict.



A node that shares a common neighbour also creates a conflict.



Therefore, the scheduler connects nodes whose shortest-path distance is:



\*\*≤ 2 hops\*\*



Each color in the conflict graph represents one TDMA slot.



\---



\## Slide 5 — Scheduling Algorithm



\### Heuristic Graph Coloring



The scheduler evaluates multiple ordering strategies:



\- Highest-degree ordering

\- Lowest-degree ordering

\- DSATUR-style ordering

\- NetworkX largest-first ordering



For each ordering:



1\. Select the next node.

2\. Check slots already used by conflicting nodes.

3\. Assign the first available slot.

4\. Compare the resulting number of slots.



The coloring using the fewest slots among the candidates is selected.



\---



\## Slide 6 — Final Results



\### Sample Topology



\- Nodes: \*\*16\*\*

\- Radio links: \*\*42\*\*

\- Conflict pairs: \*\*90\*\*

\- Slots used: \*\*9\*\*

\- Validation: \*\*PASSED\*\*

\- Distance-2 conflicts: \*\*0\*\*



\### Exact Verification



An exact backtracking verifier was also implemented.



For this sample:



\- 8 slots → Not possible

\- 9 slots → Possible



Therefore, \*\*9 slots is the minimum for this specific sample topology.\*\*



\---



\## Slide 7 — Schedule



\### Node-to-Slot Mapping



| Node | Slot |

|------|------|

| Node\_01 | 8 |

| Node\_02 | 5 |

| Node\_03 | 4 |

| Node\_04 | 8 |

| Node\_05 | 7 |

| Node\_06 | 3 |

| Node\_07 | 2 |

| Node\_08 | 7 |

| Node\_09 | 6 |

| Node\_10 | 1 |

| Node\_11 | 0 |

| Node\_12 | 6 |

| Node\_13 | 8 |

| Node\_14 | 5 |

| Node\_15 | 4 |

| Node\_16 | 8 |



\---



\## Slide 8 — Testing



\### Automated Tests



Implemented using Pytest.



Tests cover:



\- Radio graph construction

\- Distance-2 conflict detection

\- Schedule validation

\- Schedule matrix generation



\### Result



\*\*4 tests passed\*\*



The generated schedule was also checked for conflict violations.



\---



\## Slide 9 — Part 2: EMANE Integration



\### Proposed Architecture



Python Scheduler

↓

Node-to-Slot Mapping

↓

Schedule Adapter

↓

EMANE TDMA Schedule Event

↓

EMANE TDMA Radio Model

↓

Scheduled Packet Transmission



\### Prototype Completed



A Python schedule adapter converts the Node-to-Slot mapping into a generic XML schedule representation.



The prototype uses a \*\*1 ms slot duration\*\*.



\---



\## Slide 10 — Current Status and Conclusion



\### Completed



\- Distance-based radio graph

\- Distance-2 conflict graph

\- TDMA slot allocation

\- Schedule validation

\- Exact verification for sample topology

\- Automated tests

\- Part 2 schedule adapter prototype

\- Project documentation



\### Part 2 Limitation



Actual EMANE packet-level execution has not been claimed.



The XML adapter is an integration prototype; the exact EMANE event schema must match the installed EMANE version and TDMA model.



\### Conclusion



The project successfully produces and validates a conflict-free TDMA schedule for the supplied 16-node topology, with 9 slots being the minimum for that sample.

