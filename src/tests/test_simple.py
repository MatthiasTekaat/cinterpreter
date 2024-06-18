from interpreter import interpret, interpret_statements
import unittest


class Test(unittest.TestCase):
    def test_return(self):
        result, _, _ = interpret_statements("return 1;")

        self.assertEqual(result, 1)

    def test_add(self):
        result, _, _ = interpret_statements("return 1 + 2;")

        self.assertEqual(result, 3)

    def test_mul(self):
        result, _, _ = interpret_statements("return 2 * 3;")

        self.assertEqual(result, 6)

    def test_var_decl(self):
        result, _, _ = interpret_statements("int x = 3; return x;")

        self.assertEqual(result, 3)

    def test_add_var(self):
        result, _, _ = interpret_statements(
            """
        int a = 1;
        int b = 2;
        int c = a + b;
        return c;
        """
        )

        self.assertEqual(result, 3)

    def test_if_then(self):
        result, _, _ = interpret_statements(
            """
        int n;
        n = 1;
        if (n){
            return 123;
        }else{
            return -1;
        }
        """
        )

        self.assertEqual(result, 123)

    def test_if_then_else(self):
        result, _, _ = interpret_statements(
            """
        int n;
        n = 0;
        if (n){
            return -1;
        }else{
            return 123;
        }
        """
        )

        self.assertEqual(result, 123)

    def test_while(self):
        result, _, _ = interpret_statements(
            """
        int n;
        int s;
        s = 0;
        n = 10;
        while (n) {
            n = n - 1;
            s = s + n;
        }
        return s;
        """
        )

        self.assertEqual(result, sum(range(10)))

    def test_array(self):
        result, _, _ = interpret(
            """
        #include <stdlib.h>

        int main(){
            int *ptr;
            ptr = malloc(2 * sizeof(int));
            ptr[0] = 10;
            ptr[1] = 20;
            int sum;
            sum = ptr[0] + ptr[1];
            free(ptr);
            return sum;
        }
        """
        )

        self.assertEqual(result, 30)

    def test_array(self):
        result, _, _ = interpret(
            """
        #include <stdlib.h>

        int main(){
            int *ptr;
            ptr = malloc(2 * sizeof(int));
            (void)ptr;
            return 0;
        }
        """
        )

        # with self.assertRaises(MissingFreeError): besser
        self.assertNotEqual(result, 0)

    def test_ptr(self):
        result, _, _ = interpret_statements(
            """
        int *ptr;
        int a;
        a = 66;
        ptr = &a;
        *ptr = 3;
        return a;
        """
        )

        self.assertEqual(result, 3)

    def test_pointer_into_array(self):
        result, _, _ = interpret(
            """
        #include <stdlib.h>

        int main(){
            int *arr_ptr;
            int *ptr;
            arr_ptr = malloc(2 * sizeof(size_t));
            ptr = &arr_ptr[1];
            *ptr = 123;
            int result = arr_ptr[1];
            free(arr_ptr);
            return result;
        }
        """
        )

        self.assertEqual(result, 123)


if __name__ == "__main__":
    unittest.main()
