from memory import *
from datatypes import *
import struct
from errorhandler import ConversionError
from scope import Scope

#data type keys for data type (used for byte representation)
data_type_key={
    'char': 'c',
    'signed char': 'b',
    'unsigned char': 'B',
    'short': 'h',
    'unsigned short': 'H',
    'int': 'i',
    'unsigned int': 'I',
    'long': 'l',
    'unsigned long': 'L',
    'long long': 'q',
    'unsigned long long': 'Q',
    'float': 'f',
    'double': 'd',
    'size_t': 'l'

}

pointer_conversions = [
    "int_float",
    "char_int",
    "double_int",
    "int_void",
    "int_char",
    "float_double",
    "int_long",
    "int_unsignedint",
    "int_longlong",
    "struct_struct"
]

valid_assignments = [
    "",
    "int_int",
    "double_double",
    "double_double",
    "float_float",
    "char_char",
    "signedint_signedint",
    "unsignedint_unsignedint",
    "longlong_longlong",
    "longlong_double",
    "longlong_float",
    "char_int",
    "int_char"
    "int_double",
    "int_float",
    "int_long",
    "float_double",
    "float_long",
    "double_long",
    "long_longlong",
    "int_void",
    "unsignedint_int",
    "int_unsignedint",
    "signedint_int",
    "int_signedint"
]



def get_byte_representation(value, data_type,endianness="<"):
    """
        Get the byte representation of a value based on its data type.

        Parameters:
            value: The value to be represented in bytes.
            data_type: The data type of the value.
            endianness: The endianness of the byte representation.

        Returns:
            byte_representation: The byte representation of the value.
    """
    if data_type in c_data_types.keys():

        if data_type not in data_type_key.keys():
            raise DataTypeError(data_type)

        # Get the byte representation using struct
        format_string = endianness + f'{data_type_key.get(data_type)}'

        if data_type == 'char' and isinstance(value,bytes):
            value = value
        elif data_type == 'char' and isinstance(value,str):
            value = value.encode('utf-8')
        elif data_type == 'char' and not isinstance(value, str):
            value = chr(value).encode('utf-8')

        if isinstance(value,str) and data_type in ['int','unsigned char','signed char']:
            if len(value) == 1:
                value = ord(value)
            else:
                raise DataTypeError(data_type)

        if data_type=='int':
            try:
                value = int(value)
            except:
                raise ConversionError(value, data_type)

        try:
            byte_representation = struct.pack(format_string, value)
        except:
            raise ConversionError(value,data_type)
        return byte_representation
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def convert_from_byte_representation(byte_representation, data_type,endianness="<"):
    """
        Convert a byte representation back to its original value.

        Parameters:
            byte_representation: The byte representation to be converted.
            data_type: The data type of the original value.
            endianness: The endianness of the byte representation.

        Returns:
            unpacked_value: The original value obtained from the byte representation.
    """
    if data_type in c_data_types.keys():
        if data_type not in data_type_key.keys():
            raise DataTypeError(data_type)

        # Unpack the byte representation to get the original value
        format_string = endianness + f'{data_type_key.get(data_type)}'
        unpacked_value = struct.unpack(format_string, byte_representation)[0]

        return unpacked_value #ctype_type.value
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


class Value:
    def __init__(
            self,
            is_return: bool = False,
            is_break: bool = False,
            is_continue: bool = False,
            is_lvalue: bool = False,
            stars: int = 0,
            is_pointer: bool = False,

    ) -> None:
        """
                Initialize a Value object with specified attributes.

                Parameters:
                    is_return: Indicates if the value is associated with a return statement.
                    is_break: Indicates if the value is associated with a break statement.
                    is_continue: Indicates if the value is associated with a continue statement.
                    is_lvalue: Indicates if the value is an lvalue.
                    stars: The number of pointer stars associated with the value.
        """

        self.is_return = is_return
        self.is_break = is_break
        self.is_continue = is_continue
        self.is_lvalue = is_lvalue
        self.stars = stars

    def get_value(self) -> float:
        """
                Get the value of the object. Must be implemented by subclasses.

                Raises:
                    NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("get_value of Value() not implemented")

    def set_value(self, value: int, scope: Scope,offset:int,stars:int) -> None:
        """
                Set the value of the object. Must be implemented by subclasses.

                Parameters:
                    value: The value to be set.
                    offset: The offset used for setting the value.
                    stars: The number of pointer stars associated with the value.

                Raises:
                    NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError(f"{self} can not be written to")


class RValue(Value):

    def __init__(self, value: int,stars: int = 0) -> None:
        """
                    Initialize an RValue object with a specified value and number of pointer stars.

                    Parameters:
                        value: The value associated with the RValue.
                        stars: The number of pointer stars associated with the RValue.
        """
        super().__init__(stars=stars)
        self.value = value

    def get_value(self) -> int:
        """
                Get the value associated with the RValue.

                Returns:
                    int: The value of the RValue.
        """
        return self.value

    def __str__(self) -> str:
        """
                Get a string representation of the RValue.

                Returns:
                    str: The string representation of the RValue.
        """
        return f"RValue({self.get_value()})"

    __repr__ = __str__

class LValue(Value):
    def __init__(self, address: int, memory: Memory, data_type_str: str,size:int,stars: int = 0,dimension:int =1,
                 is_array=False,is_pointer=False,dimension_size=1,offset=0) -> None:
        """
                Initialize an LValue object with a specified address, memory, data type, size, number of pointer stars,
                and dimension.

                Parameters:
                    address: The memory address associated with the LValue.
                    memory: The Memory object associated with the LValue.
                    data_type_str: The data type of the LValue.
                    size: The size of the LValue.
                    is_pointer: is LValue a pointer.
                    stars: The number of pointer stars associated with the LValue.
                    dimension: The dimension of the LValue.
                    dimension_size: use to determine arrray dimension
                    offset: Helper for struct pointers to determine offset
        """
        super().__init__(is_lvalue=True, stars=stars)
        self.address = address
        self.memory = memory
        self.size = size
        self.data_type=data_type_str
        self.dimension=dimension
        self.is_array=is_array
        self.is_pointer: bool = is_pointer
        self.dimension_size=dimension_size
        self.offset=offset
        #self.read_only=read_only

    def set_new_type(self, to_type):
        """
                Changes LValue data type.

                Parameters:
                    to_type: The target data type for conversion.

                Returns:
                    The converted value based on the target data type.
        """
        try:
            if to_type == "int" and self.data_type != 'char':
                self.data_type=to_type
            elif to_type == "int" and self.data_type == 'char':
                self.data_type = to_type
            elif to_type == "float":
                self.data_type = to_type
            elif to_type == "char":
                self.data_type = to_type
            else:
                raise InterruptedError("Conversion not possible")
        except:
            raise InterruptedError("Conversion not possible")

    def type_convert(self,to_type):
        """
                Convert the LValue to the specified data type.

                Parameters:
                    to_type: The target data type for conversion.

                Returns:
                    The converted value based on the target data type.
        """
        try:
            if to_type == "int" and self.data_type != 'char':
                return int(self.get_value())
            elif to_type == "int" and self.data_type == 'char':
                return ord(self.get_value())
            elif to_type == "float":
                return float(self.get_value())
            elif to_type == "char":
                return chr(self.get_value())
            else:
                InterruptedError("Conversion not possible")
        except:
            InterruptedError("Conversion not possible")

    def get_value(self,offset=0,stars=0,is_lhs=False,size=None,data_type=None) -> int:
        """
                Get the value of the LValue.

                Parameters:
                    offset: The offset used for getting the value.
                    stars: The number of pointer stars associated with the LValue.
                    is_lhs: Indicates if the LValue is on the left-hand side of an assignment.

                Returns:
                    int: The value of the LValue.
        """

        current_address = self.address
        current_stars = self.stars
        for star in range(stars):
            #data = self.memory.read(current_address + offset, size=self.memory.random_bits_size)
            data = self.memory.read(current_address, size=self.memory.random_bits_size)
            current_address = int.from_bytes(data, byteorder=self.memory.byteorder)
            current_stars -= 1

        if current_stars < 0:
            raise ReferenceError(f"Variable at {hex(self.address)} could not be dereferenced")

        if current_stars == 0:
            if size is None:
                data = self.memory.read(current_address + offset, size=get_c_type_size(self.data_type))
                return convert_from_byte_representation(data, self.data_type)
            else:
                data = self.memory.read(current_address + offset, size=size)
                return convert_from_byte_representation(data,data_type)
        else:
            #data = self.memory.read(current_address + offset, size=self.memory.random_bits_size)
            data = self.memory.read(current_address, size=self.memory.random_bits_size,ignore_offset=True)
            return int.from_bytes(data, byteorder=self.memory.byteorder)


    def set_value(self, value,scope:Scope, offset=0,stars=0,data_type=None) -> None:
        """
                Set the value of the LValue.

                Parameters:
                    value: The value to be set.
                    offset: The offset used for setting the value.
                    stars: The number of pointer stars associated with the LValue.
                    data_type: helper for struct elements
        """
        #self.is_initialized[int(offset / get_c_type_size(self.data_type))] = True
        current_address=self.address
        scope.add_initialisation(current_address)

        current_stars=self.stars
        for star in range(stars):
            current_address = self.get_value(is_lhs=True)
            current_stars-=1

        if current_stars < 0:
            raise ReferenceError(f"Variable at {hex(self.address)} could not be dereferenced")

        #for star in range(self.stars,-1,-1):
        if current_stars == 0:
            if data_type is not None:
                data = get_byte_representation(value, data_type)
            else:
                data = get_byte_representation(value,self.data_type)
            self.memory.write(current_address+offset, data=data)
        else:
            if value != None:
                byte_array = value.to_bytes((value.bit_length() + 7) // 8, byteorder=self.memory.byteorder)
                self.memory.write(current_address,data=byte_array)



    def __str__(self) -> str:
        """
                Get a string representation of the LValue.

                Returns:
                    str: The string representation of the LValue.
        """
        stars = "*" * self.stars
        return f"LValue{stars}({self.get_value()} at address {hex(self.address)})"

    __repr__ = __str__

class RValue(Value):
    def __init__(self, value: int, stars: int = 0,data_type: str = None) -> None:
        """
                Initialize an RValue object with a specified value and number of pointer stars.

                Parameters:
                    value: The value associated with the RValue.
                    stars: The number of pointer stars associated with the RValue.
                    data_type: optional information about data_type
        """
        super().__init__(stars=stars)
        self.value = value
        self.data_type = data_type

    def get_value(self) -> float:
        """
                Get the value associated with the RValue.

                Returns:
                    float: The value of the RValue.
        """
        return self.value

    def __str__(self) -> str:
        """
                Get a string representation of the RValue.

                Returns:
                    str: The string representation of the RValue.
        """
        return f"RValue({self.get_value()})"

    __repr__ = __str__


if __name__ == "__main__":
    get_byte_representation(5, "int")
    get_byte_representation(5, "short")
    get_byte_representation(5, "long")
    get_byte_representation(5, "long long")
    get_byte_representation(5, "float")
    get_byte_representation(5, "double")
    get_byte_representation('a', "char")
    get_byte_representation(5, "size_t")

