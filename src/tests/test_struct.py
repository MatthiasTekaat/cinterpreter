from interpreter import interpret
import unittest


class TestStruct(unittest.TestCase):
    def test_duck(self):
        code = """

            struct Duck {
                int feet;
                int beak;
                int wings;
            };

            int main(){
                struct Duck donald;
                donald.feet = 2;
                donald.beak = 1;
                donald.wings = 2;

                return donald.beak;
            }

            """

        result, _, _ = interpret(code)

        self.assertEqual(result, 1)

    def test_duck_array(self):
        code = """

            struct Duck {
                int feet;
                int beak;
                int wings;
            };

            int main(){
                struct Duck ducks[2];
                struct Duck *donald = &ducks[1];

                donald->feet = 2;
                donald->beak = 1;
                donald->wings = 2;

                return donald->beak;
            }

            """

        result, _, _ = interpret(code)

        self.assertEqual(result, 1)

    def test_typedef(self):
        code = """
            typedef struct Duck Duck;

            struct Duck {
                int feet;
                int beak;
                int wings;
            };

            int main(){
                Duck ducks[2];
                Duck *daisy = &ducks[1];

                daisy->feet = 2;
                daisy->beak = 1;
                daisy->wings = 2;

                return daisy->wings;
            }
            """

        result, _, _ = interpret(code)

        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
