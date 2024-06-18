import unittest
from interpreter import *
from astconverter import *
import pycparser

class TestSuite1(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()
        self.parser= pycparser.CParser()

    def test_empty_main(self):
        code="""
            
            int main() {}
        """
        parsed_code= self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict,False)
        self.assertListEqual(list(self.interpreter.global_scope.definitions.keys()),["main"])

    def test_variable(self):
        code="""
            int a=5;
            int b=6;
        """
        parsed_code= self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict,False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(),5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_negative_int(self):
        code="""
            int a=-5;
            int b=6;
        """
        parsed_code= self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict,False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(),-5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_int_increment1(self):
        code = """
            int a=5;
            int b = a++;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 6);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 5);

    def test_int_increment2(self):
        code = """
            int a=5;
            int main(){
                a++;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 6);

    def test_int_increment3(self):
        code = """
            int a=5;
            int b = ++a;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 6);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_int_decrement1(self):
        code = """
            int a=5;
            int b=a--;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 4);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 5);

    def test_int_decrement2(self):
        code = """
            int a=5;
            int main(){
                a--;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 4);

    def test_int_decrement3(self):
        code = """
            int a=5;
            int b = --a;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 4);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 4);

    def test_unsignedint_variable(self):
        code = """
            unsigned int a=5;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);

    def test_unsignedint_pointer(self):
        code = """
            unsigned int c=5;
            unsigned int *a;
            int main(){
                a=&c;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(stars=1), 5);

    def test_short_variable(self):
        code = """
            short a=5;
            short b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_unsignedshort_variable(self):
        code = """
            unsigned short a=5;
            unsigned short b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_long_variable(self):
        code = """
            long a=5;
            long b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_unsigned_long_variable(self):
        code = """
            unsigned long a=5;
            unsigned long b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_longlong_variable(self):
        code = """
            long long a=5;
            long long b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_unsigned_longlong_variable(self):
        code = """
            unsigned long long a=5;
            unsigned long long b=6;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_float_variable(self):
        code = """
            float a=5.25;
            float b=6.25;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5.25,places=6)
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6.25,places=6)

    def test_float_variable_with_convert(self):

        code = """
            float a=(float) 5.25;
            float b=6.25f;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5.25, places=6)
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6.25, places=6)

    def test_char_variable(self):
        code = """
            char a='A';
            char b='b';
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), b'A')
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), b'b')

    def test_char_variable2(self):
        code = """
            int a='A';
            char b=65;
            int c= a + b;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 65);
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), b'A');
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 130);

    def test_unsigned_char_variable(self):
        code = """
            unsigned char a = 65;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 65)

    def test_comparison_operators(self):
        code = """
            int a = 0;
            int b = 0;
            int c = 0;
            int d = 0;
            int e = 0;
            int f = 0;
            
            int main() {
                if(1<2) {
                    a = 1;
                }
                if(5>4) {
                    b = 1;
                }
                if(2<=2) {
                    c = 1;
                }
                if(3>=3) {
                    d = 1;
                }
                if(1==1) {
                    e = 1;
                }
                if(1!=2) {
                    f = 1;
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("d").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("e").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("f").get_value(), 1)

    def test_explicit_cast_double_to_int(self):
        code = """
            int a = (int)123.5;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 123)

    def test_implicit_cast_double_to_int(self):
        code = """
            int a = 123.5;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 123)


    def test_int_array(self):
        code = """
            int intArray[3] = {1,3,9};
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=0), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=4), 3)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=8), 9)

    def test_int_array2(self):
        code = """
            int intArray[3];
            int main() {
                intArray[0] = 7;
                intArray[1] = 4;
                intArray[2] = 13; 
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=0), 7)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=4), 4)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=8), 13)

    def test_int_two_dim_array(self):
        code = """
            int arr[2][3] = {{1, 2, 3},{4, 5, 6}};
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=0), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=4), 2)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=8), 3)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=12), 4)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=16), 5)
        self.assertEqual(self.interpreter.current_scope.find_variable("arr").get_value(offset=20), 6)

    def test_int_pointer(self):
        code = """
            int a = 5;
            int *intPointer;
            int main(){
                intPointer = &a;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intPointer").get_value(stars=1), 5)

    def test_double_pointer(self):
        code = """
            int **a = 5;
            int b = 3;
            int *c=&b;
            
            int main(){
                a = &c;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(stars=2), 3)

    def test_array_pointer(self):
        code = """
            int intArray[3] = {1,3,9};
            int *arrayPtr;
            
            int main(){
                arrayPtr = intArray;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("arrayPtr").get_value(offset=0,stars=1), 1)

    def test_array_pointer2(self):
        code = """
            int intArray[3]= {7, 8, 9};
            int a;
            
            int main(){
                a = *intArray;                
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=0), 7)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=4), 8)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=8), 9)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 7)

    def test_array_pointer3(self):
        code = """
            int intArray[3] = {1,3,9};
            int *arrayPtr;
            
            int main(){
                arrayPtr = intArray;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=0), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=4), 3)
        self.assertEqual(self.interpreter.current_scope.find_variable("intArray").get_value(offset=8), 9)

    def test_struct_pointer(self):
        code = """
            struct my_struct {
                    int i;
                    int abi[3];
                    char c;
                    float f;
                    char s[30];
                };
            struct my_struct example_struct = {1, {5,6,7},'A', 3.14, "Hello World"};
            
            int main() {
                struct my_struct *zeiger = &example_struct;
                zeiger->i=5;
                zeiger->c='z';
                
                
            }
        """

        #
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("i").get_value(), 5)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=0), 5)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=4), 6)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=8), 7)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("c").get_value(), b'z')
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("example_struct").get("f").get_value(), 3.14, places=6)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=0), b'H')
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=1), b'e')
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=2), b'l')
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=3), b'l')
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=4), b'o')

    def test_struct_pointer_inside_struct(self):
        code = """
            int *ptr=NULL;
            struct my_struct {
                    int i;
                    struct my_struct *next;
                };
            struct my_struct a = {5,NULL};
            struct my_struct example_struct = {1, &a};
            

        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("i").get_value(), 1)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct", "next").get_value(stars=1, data_type='int',size=4),5)

    def test_if(self):
        code="""
            int a = 5;
            int b = 0;
            int main(){
                if(a > 1) {
                    b = 10;
                }
            }
        """
        parsed_code= self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict,False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(),5)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(),10)

    def test_while(self):
        code = """
            int a = 0;
            int main(){ 
                while(a < 5){
                    a++;
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);

    def test_for(self):
        code = """
            int a = 5;
            int main(){ 
                for(int i=0; i<5; i++){
                    a++;
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 10);

    def test_break(self):
        code = """
            int a = 0;
            int main(){ 
                while(a < 5000){
                    a++;
                    if(a > 9){
                        break;
                    }
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 10);

    def test_continue(self):
        code = """
            int a = 0;
            int kontostand = 100;
            int main(){ 
                while(a < 5000){
                    a++;
                    if(kontostand <= 0){
                        continue;
                    }
                    kontostand--;
                }
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5000);
        self.assertEqual(self.interpreter.current_scope.find_variable("kontostand").get_value(), 0);

    def test_int_addition(self):
        code = """
            int a=5;
            int b=6;
            int main(){
                a = a+b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 11);

    def test_int_addition2(self):
        code = """
            int a=5;
            int b = a+1;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 6);

    def test_double_addition(self):
        code = """
            double a=5.25;
            double b=6.25;
            double c = a + b;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 11.5);

    def test_int_subtraction(self):
        code = """
            int a=5;
            int b=3;
            int main(){
                a = a-b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 2);

    def test_double_subtraction(self):
        code = """
            double a=6.75;
            double b=5.25;
            int main(){
                a = a-b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 1.5);

    def test_int_multiply(self):
        code = """
            int a=5;
            int b=3;
            int main(){
                a = a*b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 15);

    def test_double_multiply(self):
        code = """
            double a=5.5;
            double b=3.2;
            int main(){
                a = a*b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 17.6);

    def test_int_division(self):
        code = """
            int a=18;
            int b=6;
            double c=0;
            int main(){
                c = a/b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 3.0);

    def test_int_division2(self):
        code = """
            double c = 2/4;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("c").get_value(), 0);

    def test_double_division(self):
        code = """
            double a=6.3;
            double b=2.1;
            int main(){
                a = a/b;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 3.0);

    def test_multiply_add_and_brackets(self):
        code = """
            double b = 3.5;
            double t=(3+2+4)*2*b;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("t").get_value(), 63.0);

    def test_scope(self):
        code = """
            int a=5;
            int main(){
                int a=6;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 5);

    def test_scope2(self):
        code = """
            int a=5;
            int main(){
                a=6;
            }
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(), 6);

    def  test_struct(self):
        code = """
            struct my_struct {
                    int i;
                    int abi[3];
                    char c;
                    float f;
                    char s[30];
                };
            struct my_struct example_struct = {1, {5,6,7},'A', 3.14, "Hello World"};
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("i").get_value(), 1);
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=0), 5);
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=4), 6);
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("abi").get_value(offset=8), 7);
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("c").get_value(), b'A');
        self.assertAlmostEqual(self.interpreter.current_scope.find_variable("example_struct").get("f").get_value(), 3.14, places=6);
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=0), b'H');
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=1), b'e');
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=2), b'l');
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=3), b'l');
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("s").get_value(offset=4), b'o');

    def test_struct_increment_member_variable(self):
        code = """
            struct my_struct {
                    int i;
                    int abi[3];
                    char c;
                    float f;
                    char s[30];
                };
            struct my_struct example_struct = {1, {5,6,7},'A', 3.14, "Hello World"};
            int q = ++example_struct.i;
            int b = example_struct.i++;
            
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(), 2)
        self.assertEqual(self.interpreter.current_scope.find_variable("example_struct").get("i").get_value(), 3)

    def test_malloc_array(self):
        code = """
            int size = 3;
            
            int *array = NULL;
            int *helper_array = array;
        
            int main() {
                array = (int *)malloc(size * sizeof(int));
                helper_array = array;
                array[0] = 18;
                array[1] = 4;
                array[2] = 7;
                printf("Wert von helper_array: %d", array[1]);
                printf("Wert von helper_array: %d", helper_array[1]);
                
                
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict,False)
        self.assertEqual(self.interpreter.current_scope.find_variable("helper_array").get_value(offset=4,stars=1),4)


    def test_malloc_int_pointer(self):
        code = """
            int *q;
            int main() {
                q = malloc(sizeof(int));
                *q=6;
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("q").get_value(stars=1, offset=0), 6)

    def test_assign_float_to_int(self):
        code = """
            float a = 4.5;
            int b = a;
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()
        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("b").get_value(stars=0, offset=0), 4)

    def test_global_defined_variable_is_initialized_with_zero_automatically(self):
        code = """
            int a;
            int main() {
                printf("%d", a);
            }
        """
        parsed_code = self.parser.parse(code, filename='<none>')
        ast_converter = AstConverter(parsed_code)

        ast_converter.ast_to_dict()

        self.interpreter.run(ast_converter.code_dict, False)
        self.assertEqual(self.interpreter.current_scope.find_variable("a").get_value(stars=0, offset=0), 0)

if __name__ == '__main__':
    unittest.main()