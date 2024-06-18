from interpreter import interpret
import unittest

def ackermann(m, n):
    if m == 0:
        return n + 1

    if n == 0:
        return ackermann(m - 1, 1)

    return ackermann(m - 1, ackermann(m, n - 1))

expected_values = [
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 6],
    [3, 5, 7, 9, 11],
    [5, 13, 29, 61, 125],
]

for m in range(4):
    for n in range(5):
        assert ackermann(m, n) == expected_values[m][n]

class TestFunctions(unittest.TestCase):
    def test_add(self):
        code = """
            int add(int a, int b){
                return a + b;
            }

            int main(){
                return add(6, 7);
            }
        """

        result, _, _ = interpret(code)

        self.assertEqual(result, 13)

    def test_find_min_index(self):
        code = """
            int find_min_index(int *values, int n){
                if (n <= 0) return -1;

                int min_index = 0;

                for (int i = 1; i < n; i++){
                    if (values[min_index] > values[i]){
                        min_index = i;
                    }
                }

                return min_index;
            }

            int main(){
                int values[] = {1, 2, 3, 4, 5, 6, -10, 7, 8, 9, 10};
                return find_min_index(values, 11);
            }
        """

        result, _, _ = interpret(code)

        self.assertEqual(result, 6)

    def test_ackermann(self):
        code = """
        #include <stdio.h>

        int ackermann(int m, int n){
            if (m == 0){
                return n + 1;
            } else if (n == 0){
                return ackermann(m - 1, 1);
            } else {
                return ackermann(m - 1, ackermann(m, n - 1));
            }
        }

        int main(){
            for (int m = 0; m < 4; m++){
                for (int n = 0; n < 5; n++){
                    printf("%i\\n", ackermann(m, n));
                }
            }
            return 0;
        }
        """

        result, stdout, _ = interpret(code)

        expected = "".join(f"{ackermann(m, n)}\n" for m in range(4) for n in range(5))

        self.assertEqual(stdout, expected.encode("utf-8"))

        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()

