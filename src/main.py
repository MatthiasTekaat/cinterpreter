import sys
import os
from interpreter import Interpreter
from memory import Memory
import pycparser
import pycparser_fake_libc
from astconverter import AstConverter


def parse_c_code(file):
    """
        Parse the given C code file into an Abstract Syntax Tree (AST).

        Args:
            file (str): The path to the C code file.

        Returns:
            pycparser.c_ast.FileAST: The parsed AST representing the C code.
    """
    # Setting up the arguments for the C preprocessor (cpp) with the fake libc
    fake_libc_arg = "-I" + pycparser_fake_libc.directory
    # Parsing the C code file using pycparser
    ast = pycparser.parse_file(file, use_cpp=True, cpp_args=fake_libc_arg, parser=pycparser.CParser())
    return ast


if __name__ == "__main__":
    # Retrieving the file name from command line arguments
    file_name = sys.argv[1]

    # Checking if the file exists
    if not os.path.exists(file_name):
        print(f"The file at {file_name} does not exist.")
        raise FileNotFoundError(file_name)

    try:
        # Parsing the C code file into an Abstract Syntax Tree (AST)
        parsed_code = parse_c_code(file_name)
    except:
        # Handling parsing errors
        raise Exception("File could not be parsed!")

    # Creating a Memory object for the interpreter
    memory = Memory()

    # Creating an empty dictionary to store the converted AST
    code_dict = {}

    # Creating an instance of AstConverter and converting AST to dictionary
    ast_converter = AstConverter(parsed_code)
    ast_converter.ast_to_dict()

    # Uncomment the line below if you want to print the converted dictionary
    # print(json.dumps(ast_converter.code_dict, indent=4))

    # Creating an instance of the Interpreter and running it with the converted AST
    interpreter = Interpreter()
    interpreter.run(ast_converter.code_dict)
