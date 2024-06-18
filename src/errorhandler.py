class InterpreterError(Exception):
    """
        Raised for general interpreter errors. Usually only used, when no special error is implemented so far
    """
    def __init__(self, message: str, line: int) -> None:
        super().__init__(message,line)


class AssignmentToConstObjectError(Exception):
    """
        Raised when a declaration name has an incorrect type.
    """
    def __init__(self, address,line: int = 0) -> None:
        super().__init__("Value cannot be assigned to const object at {}!",address,line)

class ConversionError(Exception):
    """
        Raised when a declaration name has an incorrect type.
    """
    def __init__(self, value, data_type,line: int = 0) -> None:
        super().__init__("Value {} cannot be interpreted as data type {}".format(value, data_type),line)

class DeclarationNameError(Exception):
    """
        Raised when a declaration name has an incorrect type.
    """
    def __init__(self, name: str, line: int = 0) -> None:
        super().__init__("Declaration for {} must be of type str but is of type {}".format(name, type(name)),line)

class InvalidConversion(Exception):
    """
        Raised when an invalid type conversion for pointers is attempted.
        """
    def __init__(self, fromT,toT, line: int) -> None:
        super().__init__("Type Conversion from {} to {} is not valid".format(fromT,toT),line)

class InvalidPointerConversion(Exception):
    """
        Raised when an invalid type conversion for pointers is attempted.
        """
    def __init__(self, line: int) -> None:
        super().__init__(f"Type Conversion for pointers is not valid,line")

class MaxRecursionDepthExceededError(Exception):
    """
        Raised when the maximal recursion depth is exceeded.
        """
    def __init__(self, max_recursion_depth: int, line: int) -> None:
        super().__init__(f"Maximal Recursion Depth of {max_recursion_depth} exceeded",line)

class MemoryOverflowError(Exception):
    """
        Raised when there is a memory overflow during variable allocation.
    """
    def __init__(self, memory_expected:int,memory_got, line: int = 0) -> None:
        super().__init__("Memory Overflow: Variable size is {} byte, but only {} byte allowed!".format(memory_got, memory_expected),line)

class UndefinedDataType(Exception):
    """
        Raised when an undefined data type is encountered.
    """
    def __init__(self, name: str, line: int = 0) -> None:
        super().__init__("DataType {} not in defined".format(name),line)

class UndefinedVariable(Exception):
    """
        Raised when an undefined variable is encountered.
    """
    def __init__(self, name: str, line: int = 0) -> None:
        super().__init__("Variable {} not in Scope".format(name),line)

class UninitializedVariable(Exception):
    """
        Raised when an uninitialized variable is accessed.
    """
    def __init__(self, name: str, line: int = 0) -> None:
        super().__init__("Variable {} not initialized".format(name),line)

class WrongArrayDimension(Exception):
    """
        Raised when an incorrect array dimension is encountered.
    """
    def __init__(self, expected_dimension: int, given_dimension: int, line: int = 0) -> None:
        super().__init__(
            "Expected dimension {} does not fit given dimension {}".format(expected_dimension, given_dimension), line)

class WrongDataType(Exception):
    """
        Raised when an incorrect data type is assigned.
    """
    def __init__(self, data_type_expected: str,data_type_got:str, line: int = 0) -> None:
        super().__init__("Expected data type {} does not fit assigned data_type {}".format(data_type_expected, data_type_got),line)

class WrongReturnType(Exception):
    """
        Raised when an incorrect return data type is encountered.
    """
    def __init__(self, data_type_expected: str,data_type_got:str, line: int = 0) -> None:
        super().__init__("Expected return data type {} does not fit actual return data_type {}".format(data_type_expected, data_type_got),line)

class WrongNumberOfArguments(Exception):
    """
        Raised when the number of arguments for a function is incorrect.
    """
    def __init__(self, expected_args: int,actual_args:int, method_name: str, line: int = 0) -> None:
        super().__init__("Expected number of args {} does not fit actual number of args {} for function".format(expected_args, actual_args, method_name),line)

class OperationNotAllowed(Exception):
    """
       Raised when an operation is not allowed.
    """
    def __init__(self, message: str, line: int = 0) -> None:
        super().__init__(message,line)