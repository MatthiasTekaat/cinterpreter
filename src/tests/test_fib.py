from interpreter import interpret
import unittest


def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


class TestFib(unittest.TestCase):
    def test_fib(self):
        for n in range(10):
            code = (
                """

            int fib(int n){
                if (n > 1){
                    int a = fib(n - 1);
                    int b = fib(n - 2);
                    int c = a + b;
                    return c;
                }else{
                    return 1;
                }
            }

            #include <stdio.h>

            int main(){
                return fib(%d);
            }

            """
                % n
            )

            result, _, _ = interpret(code)

            self.assertEqual(result, fib(n))


if __name__ == "__main__":
    unittest.main()
