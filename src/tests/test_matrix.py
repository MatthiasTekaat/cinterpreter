from interpreter import interpret
import unittest

class TestMatrix(unittest.TestCase):
    def test_matrix(self):
        with open("matrix.c") as f:
            code = f.read()

        with open("matrix_expected.txt") as f:
            expected = f.read()

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), expected)

if __name__ == "__main__":
    unittest.main()


