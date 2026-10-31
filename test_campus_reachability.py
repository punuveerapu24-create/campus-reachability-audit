#!/usr/bin/env python3
"""
Unit tests for Problem 02: Campus Reachability and Emergency Route Audit.
"""

import os
import subprocess
import sys
import unittest

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "campus_reachability.py")


class TestCampusReachability(unittest.TestCase):
    def run_solver(self, input_data: str) -> str:
        proc = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
        )
        return proc.stdout.strip()

    def test_sample_connected_graph(self):
        input_data = (
            "5 4\n"
            "0 1\n"
            "0 3\n"
            "1 2\n"
            "3 4\n"
            "0 3\n"
            "2\n"
            "4\n"
            "0\n"
        )
        expected_output = (
            "COMPONENTS 1\n"
            "LABELS 0 0 0 0 0\n"
            "DFS 0 1 2 3 4\n"
            "BFS 0 1 3 2 4\n"
            "ROUTE 2 2 0 1 2\n"
            "ROUTE 4 2 0 3 4\n"
            "ROUTE 0 0 0"
        )
        self.assertEqual(self.run_solver(input_data), expected_output)

    def test_disconnected_graph_unreachable(self):
        input_data = (
            "7 4\n"
            "0 1\n"
            "1 2\n"
            "3 4\n"
            "5 6\n"
            "3 4\n"
            "4\n"
            "0\n"
            "5\n"
            "3\n"
        )
        expected_output = (
            "COMPONENTS 3\n"
            "LABELS 0 0 0 3 3 5 5\n"
            "DFS 3 4\n"
            "BFS 3 4\n"
            "ROUTE 4 1 3 4\n"
            "ROUTE 0 UNREACHABLE\n"
            "ROUTE 5 UNREACHABLE\n"
            "ROUTE 3 0 3"
        )
        self.assertEqual(self.run_solver(input_data), expected_output)

    def test_isolated_vertices(self):
        input_data = (
            "3 0\n"
            "1 3\n"
            "0\n"
            "1\n"
            "2\n"
        )
        expected_output = (
            "COMPONENTS 3\n"
            "LABELS 0 1 2\n"
            "DFS 1\n"
            "BFS 1\n"
            "ROUTE 0 UNREACHABLE\n"
            "ROUTE 1 0 1\n"
            "ROUTE 2 UNREACHABLE"
        )
        self.assertEqual(self.run_solver(input_data), expected_output)


if __name__ == "__main__":
    unittest.main()
