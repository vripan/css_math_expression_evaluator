import unittest
from src.expr_parser import *

class ExprParserTestCases(unittest.TestCase):
    def test_rem(self):
        with_big = run_one("5 % 2 + 0", {})
        with_int = run_one("5 % 2 + 0", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 1)

    def test_unknown_token(self):
        with self.assertRaises(Exception):
            run_one("```x - 1", {"x": BigNum(0)})

    def test_missing_paren(self):
        with self.assertRaises(Exception):
            run_one("(x - 1", {})

    def test_sub_negative(self):
        with self.assertRaises(Exception):
            run_one("x - 1", {"x": BigNum(0)})

    def test_div_0(self):
        with self.assertRaises(Exception):
            run_one("2 / x", {"x": BigNum(0)})
        with self.assertRaises(Exception):
            run_one("2 % x", {"x": BigNum(0)})

    def test_complex(self):
        with_big = run_one("2 ** (1 + 2 * x - 3 / sqrt y)", {"x": BigNum(2), "y": BigNum(9)})
        with_int = int(run_one("2 ** (1 + 2 * x - 3 / sqrt y)", {"x": int(2), "y": int(9)}, int))
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 16)

    def test_vars(self):
        with_big = run_one("(x * 2 + y * z) ** t",
                           {"x": BigNum(2), "y": BigNum(3), "z": BigNum(4), "t": BigNum(2)})
        with_int = run_one("(x * 2 + y * z) ** t",
                           {"x": int(2), "y": int(3), "z": int(4), "t": int(2)}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_big, 256)

    def test_sqrt(self):
        with_big = run_one("sqrt 9 + sqrt 4", {})
        with_int = int(run_one("sqrt 9 + sqrt 4", {}, int))
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 5)

    def test_special(self):
        with_big = run_one("2 ** 3 + 5 * 6 - 3", {})
        with_int = run_one("2 ** 3 + 5 * 6 - 3", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 35)

    def test_basic(self):
        with_big = run_one("1 + 2 * 3 + 4 * 5", {})
        with_int = run_one("1 + 2 * 3 + 4 * 5", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 27)

    def test_parens(self):
        with_big = run_one("(1 + 2) * (3 + 4 * 5)", {})
        with_int = run_one("(1 + 2) * (3 + 4 * 5)", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 69)

    def test_super_basic(self):
        with_big = run_one("1 + 1", {})
        with_int = run_one("1 + 1", {}, int)
        self.assertEqual(str(with_big), str(with_int))
        self.assertEqual(with_int, 2)