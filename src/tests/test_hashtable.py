from interpreter import interpret
import unittest

class TestHashtable(unittest.TestCase):
    def test_quicksort(self):
        with open("hashtable.c") as f:
            code = f.read()

        result, _, _ = interpret(code)

        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
