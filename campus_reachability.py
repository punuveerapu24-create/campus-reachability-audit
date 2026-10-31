#!/usr/bin/env python3
"""
Problem 02: Campus Reachability and Emergency Route Audit
Design and Analysis of Algorithms (DAA) Lab Challenge

This standalone script analyzes an undirected campus walkway graph:
1. Connected Components Audit: Identifies components using recursive DFS,
   labeling each vertex with the minimum vertex index in its component.
2. Source Traversals: Performs an independent recursive DFS and queue-based BFS
   from a source vertex s, processing neighbors in ascending numerical order.
3. Shortest Path Route Audit: Reconstructs minimum-edge routes to target queries
   using BFS discovery parent pointers.
"""

from collections import deque
import sys
from typing import List, Optional, Tuple

# Prevent recursion depth errors during deep DFS traversals (n <= 200)
sys.setrecursionlimit(3000)


def compute_connected_components(n: int, adj: List[List[int]]) -> Tuple[int, List[int]]:
    """
    Identifies connected components using recursive Depth-First Search.

    Iterates through vertices from 0 to n - 1. When an unvisited vertex is encountered,
    it serves as the leader (smallest vertex index) of a new component. A recursive
    DFS traverses the component and labels all reachable vertices with this leader.

    Args:
        n: Total number of vertices (0 through n - 1).
        adj: Sorted adjacency lists for each vertex.

    Returns:
        A tuple (c, labels) where:
            c: Total count of connected components.
            labels: List of length n where labels[v] is the smallest vertex
                    number in the connected component containing v.
    """
    visited = [False] * n
    labels = [-1] * n
    component_count = 0

    def _dfs_component(u: int, label: int) -> None:
        visited[u] = True
        labels[u] = label
        for neighbor in adj[u]:
            if not visited[neighbor]:
                _dfs_component(neighbor, label)

    for v in range(n):
        if not visited[v]:
            component_count += 1
            # Iterating in ascending order guarantees v is the minimum index in this component
            _dfs_component(v, v)

    return component_count, labels


def source_dfs(s: int, n: int, adj: List[List[int]]) -> List[int]:
    """
    Performs an independent recursive DFS starting from source vertex s.
    Neighbors are visited strictly in ascending vertex-number order.
    The traversal order is recorded when first entering each vertex (pre-order).

    Args:
        s: Source vertex index.
        n: Total number of vertices.
        adj: Sorted adjacency lists for each vertex.

    Returns:
        List of vertices in the exact order they were visited.
    """
    visited = [False] * n
    dfs_order: List[int] = []

    def _dfs(u: int) -> None:
        visited[u] = True
        dfs_order.append(u)
        for neighbor in adj[u]:
            if not visited[neighbor]:
                _dfs(neighbor)

    _dfs(s)
    return dfs_order


def source_bfs(
    s: int, n: int, adj: List[List[int]]
) -> Tuple[List[int], List[int], List[Optional[int]]]:
    """
    Performs an independent queue-based BFS starting from source vertex s.
    Neighbors are visited strictly in ascending vertex-number order.
    Vertices are marked visited upon being enqueued. The BFS traversal order
    is recorded upon removing a vertex from the queue.

    Tracks shortest-path distances and first-discovery parent pointers.

    Args:
        s: Source vertex index.
        n: Total number of vertices.
        adj: Sorted adjacency lists for each vertex.

    Returns:
        A tuple (bfs_order, dist, parent) where:
            bfs_order: List of vertices in the order removed from the queue.
            dist: List of shortest-path distances (-1 if unreachable).
            parent: List of predecessor vertices on the BFS tree (None for s/unreachable).
    """
    visited = [False] * n
    dist = [-1] * n
    parent: List[Optional[int]] = [None] * n
    bfs_order: List[int] = []

    queue: deque[int] = deque()

    # Enqueue source vertex and mark visited
    visited[s] = True
    dist[s] = 0
    queue.append(s)

    while queue:
        u = queue.popleft()
        bfs_order.append(u)

        for neighbor in adj[u]:
            if not visited[neighbor]:
                visited[neighbor] = True
                dist[neighbor] = dist[u] + 1
                parent[neighbor] = u
                queue.append(neighbor)

    return bfs_order, dist, parent


def reconstruct_route(
    s: int, t: int, dist: List[int], parent: List[Optional[int]]
) -> Optional[List[int]]:
    """
    Reconstructs the minimum-edge route from s to t using BFS parent pointers.

    Args:
        s: Source vertex index.
        t: Target vertex index.
        dist: Shortest distance array computed by BFS from s.
        parent: Parent pointer array recorded during BFS discovery.

    Returns:
        List of vertices forming the path from s to t if reachable; None if unreachable.
    """
    if dist[t] == -1:
        return None

    path: List[int] = []
    curr: Optional[int] = t
    while curr is not None:
        path.append(curr)
        if curr == s:
            break
        curr = parent[curr]

    path.reverse()
    return path


def solve() -> None:
    """
    Reads campus walkway graph and audit queries from standard input (sys.stdin),
    runs the required audits and traversals, and writes output to standard output (sys.stdout).
    """
    input_text = sys.stdin.read()
    if not input_text.strip():
        return

    tokens = input_text.split()
    it = iter(tokens)

    # 1. Read Graph Specification
    n = int(next(it))
    m = int(next(it))

    adj: List[List[int]] = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # Sort each adjacency list to ensure neighbors are processed in strictly ascending order
    for u in range(n):
        adj[u].sort()

    # 2. Read Source and Route Queries
    s = int(next(it))
    q = int(next(it))
    queries: List[int] = [int(next(it)) for _ in range(q)]

    # 3. Connected Components Audit
    c, labels = compute_connected_components(n, adj)

    # 4. Source Traversals (DFS & BFS)
    dfs_order = source_dfs(s, n, adj)
    bfs_order, dist, parent = source_bfs(s, n, adj)

    # 5. Output Specifications
    # Output: COMPONENTS c
    print(f"COMPONENTS {c}")

    # Output: LABELS l0 l1 ... ln-1
    print(f"LABELS {' '.join(map(str, labels))}")

    # Output: DFS v1 v2 ...
    print(f"DFS {' '.join(map(str, dfs_order))}")

    # Output: BFS v1 v2 ...
    print(f"BFS {' '.join(map(str, bfs_order))}")

    # Output: For each target query t
    for t in queries:
        route = reconstruct_route(s, t, dist, parent)
        if route is None:
            print(f"ROUTE {t} UNREACHABLE")
        else:
            d = dist[t]
            route_str = " ".join(map(str, route))
            print(f"ROUTE {t} {d} {route_str}")


if __name__ == "__main__":
    solve()
