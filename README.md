# Campus Reachability and Emergency Route Audit

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Algorithms](https://img.shields.io/badge/Algorithms-DFS%20%7C%20BFS%20%7C%20Shortest%20Path-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A standalone, deterministic Python algorithmic tool for analyzing campus walkway graphs, auditing reachability across connected campus zones, recording exact depth-first and breadth-first search traversals, and reconstructing optimal emergency evacuation routes.

Developed as part of the **Design and Analysis of Algorithms (DAA) Lab Challenge**.

---

## 📌 Problem Overview

An undirected graph $G = (V, E)$ represents campus buildings and walkways, where vertices are indexed $0, 1, \dots, n-1$. The application performs three key algorithmic audits:

1. **Connected Components Audit**:
   - Discovers all disconnected zones across the campus using recursive Depth-First Search (DFS).
   - Each component is discovered starting at the smallest unvisited vertex.
   - Every vertex in a component is assigned the component's representative label (the minimum vertex index in that component).
2. **Deterministic Source Traversals**:
   - Independently performs recursive DFS and queue-based Breadth-First Search (BFS) from a designated emergency command/source vertex $s$.
   - **Neighbor Ordering**: Adjacent vertices are traversed strictly in ascending numerical order to ensure 100% deterministic, reproducible outputs.
   - **DFS Order**: Recorded upon initial entry to each vertex (pre-order discovery).
   - **BFS Order**: Recorded upon dequeue (`popleft`), marking vertices as visited immediately upon enqueue.
   - Traversals strictly remain within the source vertex's connected component.
3. **Emergency Route Audit (Shortest Paths)**:
   - For any query destination building $t$, reconstructs the minimum-edge walkway route from $s$ to $t$.
   - Directly backtracks through BFS discovery parent pointers $\mathcal{O}(\text{path length})$ without executing auxiliary shortest-path algorithms.

---

## 📥 Input Specification

All inputs are read directly from standard input (`sys.stdin`):

- **Line 1**: `n m` (where $n$ is the number of vertices, $m$ is the number of undirected edges).
- **Next $m$ lines**: `u v` (undirected edge connecting building $u$ and building $v$).
- **Next line**: `s q` (source building $s$, followed by $q$ target queries).
- **Next $q$ lines**: `t` (target building index for each route query).

### Constraints
- $1 \le n \le 200$
- $0 \le m \le \frac{n(n-1)}{2}$
- $1 \le q \le 200$
- No self-loops or duplicate edges.

---

## 📤 Output Specification

All outputs are written to standard output (`sys.stdout`) according to exact specifications:

1. `COMPONENTS c` — Number of connected components $c$.
2. `LABELS l_0 l_1 ... l_{n-1}` — Representative component label for each vertex $0 \le i < n$.
3. `DFS v_1 v_2 ...` — Recursive DFS visitation sequence starting at $s$.
4. `BFS v_1 v_2 ...` — Queue-based BFS visitation sequence starting at $s$.
5. For each queried target $t$:
   - If reachable: `ROUTE t d v_0 v_1 ... v_d` (where $d$ is the path distance in edge count, followed by the $d+1$ vertices along the path from $s$ to $t$).
   - If unreachable: `ROUTE t UNREACHABLE`

---

## 🚀 Quickstart & Usage

### Prerequisites
- Python 3.8 or higher.
- No third-party dependencies required (pure standard library: `sys`, `collections.deque`, `typing`).

### Execution via CLI Redirection
You can run the script by piping or redirecting an input file:

```bash
python campus_reachability.py < sample_input.txt
```

### Interactive Execution
```bash
python campus_reachability.py
```
*(Paste input and trigger EOF via `Ctrl+D` on Linux/macOS or `Ctrl+Z` then `Enter` on Windows).*

### Running Unit Tests
```bash
python -m unittest test_campus_reachability.py
```

---

## 💡 Example

### Sample Input
```text
5 4
0 1
0 3
1 2
3 4
0 3
2
4
0
```

### Sample Output
```text
COMPONENTS 1
LABELS 0 0 0 0 0
DFS 0 1 2 3 4
BFS 0 1 3 2 4
ROUTE 2 2 0 1 2
ROUTE 4 2 0 3 4
ROUTE 0 0 0
```

---

## ⚙️ Algorithmic Complexity

| Phase | Algorithm | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| Graph Construction | Adjacency List + Sort | $\mathcal{O}(V + E \log V)$ | $\mathcal{O}(V + E)$ |
| Connected Components | Recursive DFS | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ (stack) |
| Source DFS | Pre-order Recursive DFS | $\mathcal{O}(V_s + E_s)$ | $\mathcal{O}(V_s)$ (stack) |
| Source BFS | Queue-based BFS | $\mathcal{O}(V_s + E_s)$ | $\mathcal{O}(V_s)$ (queue) |
| Route Query Audit | Parent Backtracking | $\mathcal{O}(d) \le \mathcal{O}(V)$ per query | $\mathcal{O}(V)$ |
| **Total** | | **$\mathcal{O}(V + E \log V + q \cdot V)$** | **$\mathcal{O}(V + E)$** |

---

## 📁 Repository Structure

```
campus-reachability-audit/
├── .gitignore                    # Python gitignore configuration
├── campus_reachability.py        # Core algorithm implementation
├── test_campus_reachability.py   # Automated unit test suite
└── README.md                     # Comprehensive project documentation
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
