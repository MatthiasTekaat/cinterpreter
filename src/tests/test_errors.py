from interpreter import interpret, interpret_statements
import unittest


class TestErrors(unittest.TestCase):
    def test_multiplication(self):
        code = """
        #include <stdint.h>
        #include <stdio.h>

        int main(){
            int32_t x = 123456;

            int32_t y = x * x;

            printf("%d\\n", y);

            return 0;
        }
        """
        
        with self.assertRaises(OverflowError):
            interpret(code)

    def test_addition(self):
        code = """
        #include <stdint.h>
        #include <stdio.h>

        int main(){
            int32_t x = 0x7fffffff;

            int32_t y = x + 1;

            printf("%d\\n", y);

            return 0;
        }
        """
        
        with self.assertRaises(OverflowError):
            interpret(code)

    def test_negation(self):
        code = """
        #include <stdint.h>
        #include <stdio.h>

        int main(){
            int32_t x = 0x80000000;

            int32_t y = -x;

            printf("%d\\n", y);

            return 0;
        }
        """
        
        with self.assertRaises(OverflowError):
            interpret(code)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            interpret_statements("return 1 / 0;")

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            interpret_statements("return 1 % 0;")

    def test_shift_left(self):
        # Shifting into the sign bit is undefined behavior
        code = """
        #include <stdint.h>
        #include <stdio.h>

        int main(){
            int32_t x = 0x7fffffff;

            int32_t y = x << 1;

            printf("%d\\n", y);

            return 0;
        }
        """
        
        with self.assertRaises(OverflowError):
            result, _, _ = interpret(code)

    def test_shift_right(self):
        # Shifting out of the sign bit is undefined behavior
        code = """
        #include <stdint.h>
        #include <stdio.h>

        int main(){
            int32_t x = 0x80000000;

            int32_t y = x >> 1;

            printf("%d\\n", y);

            return 0;
        }
        """
        
        with self.assertRaises(OverflowError):
            result, _, _ = interpret(code)

    def test_oob_array_access(self):
        with self.assertRaises(InvalidMemoryAccessError):
            interpret_statements("int8_t x[1]; return x[1];")

    def test_oob_array_access_negative(self):
        with self.assertRaises(InvalidMemoryAccessError):
            interpret_statements("int8_t x[1]; return x[-1];")

    def test_null_pointer_dereference(self):
        with self.assertRaises(NullPointerException):
            interpret_statements("uint8_t *x = (int*)0; return *x;")

    def test_use_after_free(self):
        code = """
        #include <stdlib.h>

        int main(){
            int *x = malloc(sizeof(int));
            free(x);
            *x = 0;
            return 0;
        }
        """

        with self.assertRaises(UseAfterFreeError):
            interpret(code)
    
    def test_uninitialized_variable(self):
        with self.assertRaises(UninitializedError):
            interpret_statements("int x; return x;")
    
    def test_uninitialized_array(self):
        with self.assertRaises(UninitializedError):
            interpret_statements("int x[1]; return x[0];")

    def test_uninitialized_malloc(self):
        code = """
        #include <stdlib.h>

        int main(){
            int *x = malloc(sizeof(int));
            int x0 = *x;
            return x0;
        }
        """

        with self.assertRaises(UninitializedError):
            interpret(code)
    
    def test_uninitialized_struct(self):
        with self.assertRaises(UninitializedError):
            interpret_statements("struct { int x; } s; return s.x;")
    
    def test_uninitialized_malloc_struct(self):
        code = """
        #include <stdlib.h>

        struct Duck {
            int x;
        }

        int main(){
            struct Duck *ducks = malloc(sizeof(struct Duck) * 2);
            Duck *duck1 = ducks + 1;
            return duck1->x;
        }
        """

        with self.assertRaises(UninitializedError):
            interpret(code)

    def test_missing_zero_termination(self):
        code = """
        #include <string.h>

        int main(){
            char s[5] = {'H', 'e', 'l', 'l', 'o'};
            int n = (int)strlen(s);
            return n;
        }
        """

        with self.assertRaises(InvalidMemoryAccessError):
            interpret(code)
    
    def test_modify_string_literal(self):
        # String literals must not be modified
        code = """
        #include <string.h>

        int main(){
            char *s = "Hello";
            s[0] = 'h';
            return 0;
        }
        """

        with self.assertRaises(InvalidMemoryAccessError):
            interpret(code)

if __name__ == "__main__":
    unittest.main()
 
