import unittest

from project_name.Calculator import Calculator


class TestCalculator(unittest.TestCase):
    def test_add_one(self):
        calculator = Calculator()
        self.assertEqual(calculator.add_one(1), 2)

    def test_add_two(self):
        calculator = Calculator()
        self.assertEqual(calculator.add_two(1), 3)


if __name__ == '__main__':
    unittest.main()
