from interpreter import interpret
import unittest

class TestLinkedList(unittest.TestCase):
    def test_singly_linked_list(self):
        with open("linked_list.c") as f:
            code = f.read()

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), "3 1 4 1 5 9 2 6 5 ")

    def test_doubly_linked_list(self):
        with open("doubly_linked_list.c") as f:
            code = f.read()

        with open("doubly_linked_list_expected.txt") as f:
            expected = f.read()

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), expected)

if __name__ == "__main__":
    unittest.main()


