import unittest
from src.ui_bridge import *

class UiBridgeTestCases(unittest.TestCase):
    def test_one_and_only_usecase(self):
        backend = BackendBridge()
        (result, output) = backend.compute_data("1+a", [("a", 1)], 10)
        self.assertEqual(result, "2")