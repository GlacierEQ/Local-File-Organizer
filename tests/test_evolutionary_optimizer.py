import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from performance import PerformanceOptimizer
from config import Config
from database import Database


class DummyDatabase(Database):
    def __init__(self):
        pass


class DummyConfig(Config):
    def __init__(self):
        pass


def dummy_operations():
    return [
        {"source": f"/dir{i}/file{i}.txt", "destination": f"/dest{i}/file{i}.txt"}
        for i in range(5)
    ]


class TestEvolutionaryOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = PerformanceOptimizer(DummyConfig(), DummyDatabase())

    def test_evolutionary_optimize_file_order(self):
        ops = dummy_operations()
        optimized = self.optimizer.evolutionary_optimize_file_order(
            ops, generations=5, population_size=10
        )
        self.assertEqual(len(optimized), len(ops))


if __name__ == "__main__":
    unittest.main()
