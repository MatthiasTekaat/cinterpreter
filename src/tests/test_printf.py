from interpreter import interpret
import unittest


class TestPrintf(unittest.TestCase):
    def test_printf(self):
        code = """
        #include <stdio.h>

        int main(){
            printf("Hello, World!\\n");
            return 0;
        }
        """

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), "Hello, World!\n")

    def test_print_int(self):
        code = """
        #include <stdio.h>

        int main(){
            printf("Hello, number %d!\\n", 5);
            return 0;
        }
        """

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.decode("utf-8"), "Hello, number 5!\n")

    def test_print_mixed(self):
        code = """
        #include <stdio.h>

        int main(){
            printf("Number: %d\\nString: %s\\nFloat: %.5f\\n", 3, "Hello", 0.125);
            return 0;
        }
        """

        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)

        expected = "Number: 3\nString: Hello\nFloat: 0.12500\n"

        self.assertEqual(stdout.decode("utf-8"), expected)

    def test_stderr(self):
        code = """
        #include <stdio.h>

        int main(){
            fprintf(stderr, "This should be printed on stderr.");
            return 0;
        }
        """

        result, _, stderr = interpret(code)

        self.assertEqual(result, 0)
        self.assertEqual(stderr.decode("utf-8"), "This should be printed on stderr.")

    def test_strlen(self):
        code = """
        #include <stddef.h>

        size_t strlen(const char *c){
            size_t n = 0;
            for (; *c; c++) n++;
            return n;
        }

        int main(){
            const char *s = "Hello";
            size_t n = strlen(s);
            int n_int = (int)n;
            return n_int;
        }
        """

        result, _, _ = interpret(code)

        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()
