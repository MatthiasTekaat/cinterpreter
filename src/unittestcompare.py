import unittest
from interpreter import *
from astconverter import *
import pycparser

class TestAddition(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()
        self.parser= pycparser.CParser()

    def test_read_freed_int_pointer_throws_exception(self):
        code = """
            int *q;
            int main() {
                q = malloc(sizeof(int));
                *q=6;
                free(q);
                printf("%d", *q);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_double_free_throws_exception(self):
        code = """
            int *q;
            int main() {
                q = malloc(sizeof(int));
                *q=6;
                free(q);
                free(q);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_not_supported_datatype_throws_exception(self):
        code = """
            signed int a = 1;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(DataTypeError, self.interpreter.run, ast_converter.code_dict, False)

    def test_using_uninitialized_variable_throws_exception(self):
        code = """
            int main() {
                int a;
                printf("%d", a);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(UninitializedVariable, self.interpreter.run, ast_converter.code_dict, False)

    def test_invalid_pointer_conversion_throws_exception(self):
        code = """
            int *intPtr;
            int *intPtr2 = 3;
            int main() {
                intPtr = (double *)intPtr2;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(InvalidConversion, self.interpreter.run, ast_converter.code_dict, False)

    def test_dividing_by_zero_throws_exception(self):
        code = """
            int a=18;
            int b=0;
            double c=0;
            int main(){
                c = a/b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(ZeroDivisionError, self.interpreter.run, ast_converter.code_dict, False)

    def test_array_write_out_of_memory_throws_exception(self):
        code = """
            int intArray[3] = {1,3,9,11};
            int main() {
                printf("%d", intArray[2]);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_array_read_out_of_memory_throws_exception(self):
        code = """
            int intArray[3] = {1,3,9};
            int main() {
                printf("%d", intArray[3]);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    def test_integer_overflow_throws_exception(self):
        code = """
            int a = 2147483647;
            int b = 2;
            int result;
            int main(){
                result = a+b;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(ConversionError, self.interpreter.run, ast_converter.code_dict, False)

    def test_shift_into_bit_sign_throws_exception(self):
        code = """
            int a = -2147483648;
            int main() {
                a = a--;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(ConversionError, self.interpreter.run, ast_converter.code_dict, False)

    def test_func_without_valid_return_throws_exception(self):
        code = """
            int b;
            void funcWithoutReturn(int a){
                a = a+1;
            }
            
            int main(){
                b = funcWithoutReturn(13);
                printf("%d", b);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(ConversionError, self.interpreter.run, ast_converter.code_dict, False)

    def test_looping_from_one_array_into_another_throws_exception(self):
        code = """
            int array1[3] = {1, 1, 1};
            int array2[3] = {2, 2, 2};

            int main() {
                for(int i=0; i<5; i++){
                    printf("%i", array1[i]);
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(MemoryError, self.interpreter.run, ast_converter.code_dict, False)

    # Funktioniert noch nicht
    def test_printing_invalid_chararray_throws_exception(self):
        code = """
            void foo(char **string){
                char local[] = "Hello, World!";
                *string = local;
            }

            int main() {
                char *string;
                foo(&string);
                
                printf("String content: %s", string);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(UninitializedVariable, self.interpreter.run, ast_converter.code_dict, False)

    def test_printing_invalid_chararray_throws_exception2(self):
        code = """
            void foo(int **array){
                int array1[3] = {1, 1, 1};
                int array2[3] = {2, 2, 2};

                *array = array1;
            }

            void bar(int *array){
                int initialized[6] = {6, 66, 666, 6666, 66666, 666666};
    
                for (int i = 0; i < 3; i++){
                    int value = array[i];

                    printf("%i", value);
                }
            }

            int main() {
                int *array;
                foo(&array);
                bar(array);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.assertRaises(UninitializedVariable, self.interpreter.run, ast_converter.code_dict, False)


if __name__ == '__main__':
    unittest.main()