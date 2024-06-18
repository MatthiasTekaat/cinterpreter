import unittest
from interpreter import *
from astconverter import *
import pycparser
import math

class TestCrucial(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()
        self.parser= pycparser.CParser()
    def test_type_conversion(self):
        code = """
            int a = 2147483647;
            long long b = 1;
            long long c;

            int main(){
                long long tmp[1] = {a + b};
                c = tmp[0];
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        c = self.interpreter.current_scope.find_variable("c").get_value()
        print(c)
        self.assertEqual(c, 2**31)

    def test_static_storage_duration(self):
        code = """int arr[2];
             int x;

             int a;
             int b;
             int c;

             int main(){
                 a = arr[0];
                 b = arr[1];
                 c = x;
             }
         """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("x").get_value(), 0)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 0)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 0)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 0)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=0), 0)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=4), 0)

    def test_array_pointer4(self):
        code = """int intArray[3] = {1,3,9};
            int *arrayPtr;
            int a;
            int b;
            int c;

            int main(){
                arrayPtr = intArray;
                a = *arrayPtr;
                b = arrayPtr[1];
                c = *(arrayPtr + 2);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=0), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=4), 3)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=8), 9)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 3)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 9)

    def test_struct_member_read(self):
        code = """
            struct my_struct {
                int i;
            };
            struct my_struct example_struct = {7};
            int a;

            int main(){
                a = example_struct.i;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 7)



    def test_2d_array(self):
        code = """
            int arr[4][5];
            int a;

            int main(){
                arr[0][0] = 3;
                a = arr[0][0];
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 3)


    def test_2d_array_invalid_read(self):
        code = """
            int arr[4][5];

            int main(){
                arr[1][7] = 3;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_struct_pointer_read(self):
        code = """
            struct my_struct {
                int x;
                int i;
            };
            struct my_struct example_struct = {2, 7};
            int a;

            int main(){
                struct my_struct *ptr = &example_struct;
                a = ptr->i;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 7)

    def test_2d_array_invalid_read(self):
        code = """
            int arr[4][5];

            int main(){
                arr[1][7] = 3;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_modify_string_literal(self):
        #const char *c = {'a','b'};
        code = """
            const char *c = "Hello, World!";
            

            int main(){
                c[0] = 0;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.assertRaises(AssignmentToConstObjectError, self.interpreter.run, ast_converter.code_dict, False)

    def test_uninitialized(self):
        code = """
            int main(){
                int uninitialized;
                int a;
                int *ptr;

                ptr = &uninitialized;
                a = *ptr;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(UninitializedVariable, self.interpreter.run, ast_converter.code_dict, False)

    def test_uninitialized_struct_pointer_read(self):
        code = """
            int main(){
                struct my_struct {
                    int i;
                };
                struct my_struct example_struct;
                int a;

                struct my_struct *ptr = &example_struct;
                a = ptr->i;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.assertRaises(UninitializedVariable, self.interpreter.run, ast_converter.code_dict, False)

    def test_ptr_read(self):
        code = """
            int x = 123;
            int a;
            int *ptr;

            int main(){
                ptr = &x;
                a = *ptr;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 123)

    def test_void_ptr_conversion(self):
        code = """
            int x = 123;
            int a;
            int *ptr;
            void *void_ptr;

            int main(){
                void_ptr = &x;
                ptr = void_ptr;
                a = *ptr;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 123)

    def test_divide_zero_zero(self):
        code = """
            double d;
            int main(){
                d = 0.0 / 0.0;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)

        self.assertEqual(self.interpreter.current_scope.find_variable("d").get_value(), float("inf"))

    def test_divide_one_zero(self):
        code = """
            double d;
            int main(){
                d = 1.0 / 0.0;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)

        self.assertEqual(self.interpreter.current_scope.find_variable("d").get_value(), float("inf"))

    def test_divide_one_minus_zero(self):
        code = """
            double d;
            int main(){
                d = 1.0 / -0.0;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)

        self.assertEqual(self.interpreter.current_scope.find_variable("d").get_value(), float("-inf"))

    def test_char_ptr_conversion(self):
        code = """
            int x = 123;
            int a;
            int *ptr;
            char *char_ptr;

            int main(){
                char_ptr = (char*)&x;
                ptr = (int*)char_ptr;
                a = *ptr;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 123)

    def test_struct_pointer_cast_write(self):
        code = """
               int j=5;
               struct my_struct {
                   int x;
                   int i;
               };
               struct my_struct example_struct = {2, 7};

               int main(){
                   
                   char *void_ptr = (char*)&example_struct;
                   struct my_struct *ptr = (struct my_struct*)void_ptr;
                   ptr->i = 5;
                   j=example_struct.i;
                   
               }
           """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("j").get_value(), 5)


if __name__ == '__main__':
    unittest.main()
