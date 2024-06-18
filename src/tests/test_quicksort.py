from interpreter import interpret
import unittest

class TestQuicksort(unittest.TestCase):
    def test_quicksort(self):
        with open("quicksort.c") as f:
            code = f.read()

        with open("quicksort_expected.txt") as f:
            expected = f.read()

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), expected)

if __name__ == "__main__":
    unittest.main()
