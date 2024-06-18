import datatypes
import memory
from value import Value,RValue,LValue
from scope import Scope
from errorhandler import *
from memory import *
from pycparser import c_ast
from datatypes import *


from value import pointer_conversions, valid_assignments

def array_multiply(arr):
    result = 1
    for num in arr:
        result *= num
    return result

class Interpreter:
    """
    Class for interpreting C code AST.

    Attributes:
        global_scope (Scope): The global scope of the interpreter.
        current_scope (Scope): The current scope being interpreted.
        memory (Memory): The memory manager for the interpreter.
        current_line (int): The current line number being interpreted.
        current_recursion_depth (int): The current recursion depth.
        max_recursion_depth (int): The maximum recursion depth allowed.
    """
    def __init__(self,random_bits_size=128) -> None:
        """
                Initialize the Interpreter class.

                Parameters:
                    random_bits_size (int): Size of random bits.

                Returns:
                    None
        """
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.memory = Memory()
        self.current_line=0
        self.current_recursion_depth=0
        self.max_recursion_depth=100000000


    def freeMemory(self,scope):
        """
                Free memory allocated to variables in a given scope.

                Parameters:
                    scope (Scope): The scope to free memory from.

                Returns:
                    None
        """
        for variable,address in scope.variables.items():
            if isinstance(address,dict):
                for var in address.values():
                    self.memory.free(var.address)
            else:
                self.memory.free(address.address)
        scope.variables={}

    def interpret(self, node: dict) -> Optional[Value]:
        """
                Interpret an AST node and perform corresponding actions.

                Parameters:
                    node (dict): The AST node to interpret.

                Returns:
                    Optional[Value]: The result of interpretation.
        """
        assert isinstance(node, dict)
        if 'line' in node:
            self.line=node['line']

        if node["node_type"] == "Return":
            # Interpret the value to be returned
            value = self.interpret(node['value'])
            # If the value is a variable name, find its value in the current scope
            if isinstance(value, str):
                value = self.current_scope.find_variable(value)
            # Ensure that the value is an instance of Value
            if not isinstance(value, Value):
                raise InterpreterError(f"Return Value {value} is not a value", self.line)
            # Mark the value as a return value
            value.is_return = True
            return value

        elif node['node_type'] == "ID" or node['node_type'] == "Typename":
            # If the node represents an identifier or a type name, return the name
            if node['name'] == 'NULL':
                return RValue(0)
            else:
                return node['name']

        elif node['node_type'] == "Cast":
            # Perform a type cast operation
            type_name=node['to_type']['name']
            type_stars = node['to_type']['stars']
            value = self.interpret(node['expression'])


            # If the value is a variable name, find its value in the current scope
            if isinstance(value,str):
                value=self.current_scope.find_variable(value)
                # Handle type conversion for pointers
                if type_stars == 0:
                    return RValue(value.type_convert(type_name))
                else:


                    if self.current_scope.is_defined(type_name):
                        left = value.data_type
                        for member in self.current_scope.get_scope(type_name)[type_name]["declaration"]:
                            right = member.get("data_type").replace(" ", "")
                            conversion_type = left + "_" + right
                            conversion_type1 = right + "_" + left
                            if not conversion_type in pointer_conversions and not  conversion_type1 in pointer_conversions:
                                raise InvalidPointerConversion(self.current_line)
                    else:
                        left = type_name.replace(" ", "")
                        right = value.data_type.replace(" ", "")
                        conversion_type = left + "_" + right
                        conversion_type1 = right + "_" + left
                        if not conversion_type in pointer_conversions and not conversion_type1 in pointer_conversions:
                            raise InvalidPointerConversion(self.current_line)
                    new_lvalue=LValue(value.address,value.memory,right,value.size,value.stars,value.dimension,value.is_array,value.is_pointer,value.dimension_size,value.offset)
                    new_lvalue.data_type=left
                    return new_lvalue
            elif isinstance(value,RValue) and type_stars >=1:
                if value.data_type is None:
                    value.data_type=type(value.get_value()).__name__
                left = type_name.replace(" ", "")
                right = value.data_type.replace(" ", "")
                conversion_type = left + "_" + right
                conversion_type1 = right + "_" + left
                if conversion_type in pointer_conversions or conversion_type1 in pointer_conversions or left == right:
                    return value.get_value()
                else:
                    raise InvalidPointerConversion(self.current_line)
            else:
                # Perform type conversion based on the target type
                if isinstance(value,list):
                    total_list=[]
                    left = type_name.replace(" ", "")
                    for val in value:

                        right = val.data_type.replace(" ", "")
                        conversion_type = left + "_" + right
                        conversion_type1 = right + "_" + left
                        if conversion_type in pointer_conversions or conversion_type1 in pointer_conversions or left == right:
                            total_list.append(val.get_value())
                        else:
                            raise InvalidPointerConversion(self.current_line)
                    return RValue(total_list[0])

                try:
                    if type_name == "int" and not isinstance(value,str):
                        return RValue(int(value.get_value()))
                    elif type_name == "int" and isinstance(value,str):
                        return RValue(ord(value.get_value()))
                    elif type_name == "float":
                        return RValue(float(value.get_value()))
                    elif type_name == "char":
                        return RValue(chr(value.get_value()))
                    else:
                        InterruptedError("Conversion not possible")
                except:
                    InterruptedError("Conversion not possible")
            # Set the data type of the resulting value
            value.data_type = type_name

        elif node["node_type"] == "Constant":
            # Handle interpretation of a constant node
            value = node['value']
            # Check if the data type of the constant is valid
            if node['data_type'] not in c_data_types.keys() and node['data_type'] != "string":
                raise DataTypeError(node['data_type'],self.line)

            # If the data type is not string, return a single RValue
            if node['data_type'] != "string":
                return RValue(value)
            else:

                ##NEW
                length=len(value)
                address = self.memory.malloc(size=self.memory.random_bits_size,)
                string_value=LValue(address,self.memory,'char',size=self.memory.random_bits_size,stars=0,is_array=True,dimension_size=length)
                offset=0
                for c in value:
                    self.current_scope.add_read_onlys(address + offset)
                    string_value.set_value(c,self.current_scope,offset,0)
                    offset +=1

                if node.get('return_value', 'rvalue') == 'lvalue':
                    return string_value
                else:
                    return RValue(address)
                    ####
                    # If the data type is string, return a list of RValues for each character
                    #return_value=[]
                    #for c in value:
                    #    return_value.append(RValue(c))
                #return return_value

        elif node["node_type"] == "Decl":
            # Handle interpretation of a declaration node
            name = node['name']
            stars= node['stars']

            #check if variable is an array and set data type
            is_array=node.get('is_array',False)
            data_type=node['data_type']

            # Validate the name of the declaration
            if not isinstance(name,str):
                raise DeclarationNameError(name,self.line)

            #get dimensions for an array
            factor=1
            dimension=1
            dimension_size=1
            if "dimension" in node:
                dimension = len(node['dimension'])
                dimension_size = node['dimension']

                factor = 1
                for x in node['dimension']:
                    factor = x*factor

            # Calculate the size of the declared variable
            if stars == 0:
                #case of a normal variable
                size=0
                total_size=0
                if data_type in c_data_types:
                    size = factor*datatypes.get_c_type_size(data_type)

                elif self.current_scope.is_defined(data_type):
                    definitions = self.current_scope.get_scope(data_type)
                    current_address = None

                    for variable in definitions.get(data_type).get("declaration"):
                        if current_address is not None and variable['stars']==0:
                            variable['sibling_address']=current_address
                            variable['total_size'] = total_size

                        variable['parent'] = name
                        variable_value=self.interpret(variable)

                        #self.memory.read(variable_value.address, variable_value.size)
                        if current_address is None:
                            current_address = variable_value.address
                        total_size +=variable_value.size
                        value=None

            else:
                #case of a pointer
                size = 0
                total_size=0
                if data_type in c_data_types:
                    size = self.memory.random_bits_size
                elif self.current_scope.is_defined(data_type):
                    size = self.memory.random_bits_size
                    definitions = self.current_scope.get_scope(data_type)
                    #variable = definitions.get(data_type).get("declaration")[0]
                    #allocate_new_mem=Truexd
                    #current_address= None

                    #for variable in definitions.get(data_type).get("declaration"):
                    #    size += c_data_types.get(variable.data_type)
                    #if current_address is not None:
                    #    variable['sibling_address']=current_address
                    #variable['parent'] = name
                    #variable['stars'] = stars
                    #variable['allocate_new_mem']=allocate_new_mem
                    #variable['total_size'] = total_size

                    #    current_variable=self.interpret(variable)
                    #    current_address=current_variable.address
                    #total_size= c_data_types.get(current_variable.data_type)
                    #allocate_new_mem=False
                    #    value=None
                #elif data_type in self.global_scope.definitions:
                #    for variable in self.global_scope.definitions.get(data_type).get("declaration"):
                #        variable['parent'] = name
                #        variable['stars'] = stars
                #        self.interpret(variable)
                #        value=None

            # Check if the data type of the declaration is valid
            if node['data_type'] not in c_data_types.keys() and not self.current_scope.is_defined(data_type):
                #and data_type not in self.global_scope.definitions and data_type not in self.current_scope.definitions:
                raise DataTypeError(node['data_type'],self.line)

            # Allocate memory for the declared variable and create an LValue
            if size>0:
                #allocate memory
                #allocate_new_mem=node.get('allocate_new_mem',True)
                if "sibling_address" in node:
                    sibling_address = node['sibling_address']
                else:
                    sibling_address = 0

                if "total_size" in node:
                    total_size = node['total_size']
                else:
                    total_size = 0
                if stars == 0 or sibling_address==0:
                    address=self.memory.malloc(size,sibling_address)
                else:
                    address=sibling_address+total_size
                if data_type =='int' and self.current_scope == self.global_scope:
                    self.current_scope.add_initialisation(address)
                #create an lvalue
                if node['rights'] == "const":
                    read_only=True
                else:
                    read_only=False

                value = LValue(address+total_size, self.memory, data_type, size, stars,dimension,is_array,dimension_size=dimension_size)
                if read_only:
                    address=value.address
                    self.current_scope.add_read_onlys(address)

                #check if variable is a pointer
                if value is not None:
                    value.is_pointer = True if stars > 0 else False

                value_map=self.current_scope.variables
                ref=value_map

                #case, when it is a struct (then parent exists)
                if "parent" in node:
                    if node['parent'] not in value_map:
                        value_map[node['parent']]={}
                    ref = value_map.get(node['parent'])
                ref[name] = value

            if value is not None:
                value.is_pointer = True if stars > 0 else False


            # Interpret statements within the declaration node, if any
            if "statements" in node:
                for statement in node['statements']:
                    self.interpret(statement)
            return value

        elif node['node_type'] == "UnaryOp":
            # Handle interpretation of a unary operation node
            expression= node['expression'].copy()
            expression['find_variable'] = True
            operation = node['operation']
            if operation == "-":
                # Interpretation of address-of operator (&)
                value = self.interpret(expression)
                if isinstance(value,str):
                    return -self.current_scope.find_variable(value).get_value()
                else:
                    # Otherwise, return the address as an RValue
                    return -value.get_value()
            if operation == "&":
                # Interpretation of address-of operator (&)
                variable=self.current_scope.find_variable(self.interpret(expression))
                if isinstance(variable,dict):
                    # If variable is a dictionary, return a list of RValues for each address
                    #return [RValue(x.address,data_type=x.data_type) for x in variable.values()]
                    item = next(iter(variable.values()))
                    return RValue(item.address,data_type=item.data_type)
                else:
                    # Otherwise, return the address as an RValue
                    return RValue(variable.address,data_type=variable.data_type)
            if operation == "*":
                # Interpretation of dereference operator (*)
                variable_find = expression
                if "is_assignment" in node:
                    # Check if the dereference operation is part of an assignment
                    stars=0
                    while "expression" in expression.keys():
                        expression = expression['expression']

                    variable_find = expression

                    while "lhs" in variable_find.keys():
                        variable_find = variable_find['lhs']

                else:
                    #non-asssignment case
                    stars =1
                    #find varaibel by looping through nested expressions
                    #number of expressions = stars
                    while "expression" in expression.keys():
                        expression = expression['expression']
                        stars+=1
                        variable_find = expression

                    #handle + Operation for pointer and arrays
                    if "operation" in expression.keys() and (expression['operation'] != "+" and expression['operation'] != "*"):
                        raise OperationNotAllowed("Formally dereferencing was called, which online allows + as binary operation",node["line"])
                    if ("operation" not in expression.keys() or expression['operation'] == "+") and ('operation' in expression.keys() and expression['operation'] != "*"):
                        stars -=1

                    while "lhs" in variable_find.keys():
                        variable_find = variable_find['lhs']

                # Find the variable to be dereferenced
                variable = self.current_scope.find_variable(self.interpret(variable_find))
                variable_find['node_type'] = 'Constant'
                variable_find['data_type'] = 'int'
                variable_find['value'] = 0

                # Calculate the offset for dereferencing
                offset = self.get_value(self.interpret(expression)) * c_data_types.get(variable.data_type)
                if "is_assignment" in node:
                    # If part of an assignment, return the variable and offset
                    return [variable, offset]
                else:
                    # Otherwise, return the value at the dereferenced address as an RValue
                    if variable.is_array:
                        stars -=1
                    if variable.is_pointer:
                        stars = max(1,stars)

                        my_variable = variable.get_value(offset=0, stars=stars-1)
                        if not self.current_scope.is_initialized(my_variable):
                            raise UninitializedVariable(variable_find,self.current_line)


                    return RValue(variable.get_value(offset=offset, stars=stars))

            elif operation == "sizeof":
                # Interpretation of sizeof operator
                return RValue(c_data_types.get(self.interpret(expression)))

            elif operation in ['p++','++','p--','--']:
                # Interpretation of increment and decrement operators
                value = self.interpret(expression)
                if isinstance(value,LValue):
                    variable = value
                elif isinstance(value,RValue):
                    variable = value
                else:
                    variable = self.current_scope.find_variable(value)

                if operation == "p++":
                    # Post-increment
                    return_value = variable.get_value()
                    variable.set_value(return_value+1,self.current_scope)
                    return RValue(return_value)
                elif operation == "p--":
                    # Post decrement
                    return_value = variable.get_value()
                    variable.set_value(return_value - 1,self.current_scope)
                    return RValue(return_value)
                elif operation == "++":
                    # Pre-increment
                    return_value = variable.get_value()+1
                    variable.set_value(return_value,self.current_scope)
                    return RValue(return_value)
                elif operation == "--":
                    # Pre decrement
                    return_value = variable.get_value()-1
                    variable.set_value(return_value,self.current_scope)
                    return RValue(return_value)
            else:
                raise InterpreterError("Unsupported operation", self.line)

        elif node['node_type'] == "StructRef":
            #Handle Struct Reference
            #case that variable should be returned
            if node.get("find_variable", True):
                if node.get("sub_type", "") == "->":
                    data_type = str(self.current_scope.find_variable(self.interpret(node["name"])).data_type)
                    members = self.current_scope.get_scope(data_type)[data_type]['declaration']
                    offset = 0
                    for member in members:
                        if "dimension" in member:
                            dimValue = array_multiply(member['dimension'])
                        else:
                            dimValue = 1
                        size = get_c_type_size(member['data_type'])*dimValue

                        if member['name'] == self.interpret(node['field']):

                            value = self.current_scope.find_variable(self.interpret(node["name"]))
                            return_value = LValue(value.address, value.memory,value.data_type,value.size,value.stars,value.dimension, value.is_array, value.dimension_size, value.offset)
                            if 'is_assignment' in node:
                                return_value.offset=offset
                                return_value.data_type=member['data_type']
                                return return_value
                            else:
                                return value.get_value(stars=1,offset=offset,size=4,data_type=member['data_type'])

                        offset +=size

                else:
                    value = self.current_scope.find_variable(self.interpret(node["name"]), self.interpret(node['field']))
                    return value

                if node.get("sub_type","") == "->":
                    if not 'is_assignment' in node:
                        if self.current_scope.is_initialized(value.get_value()):
                            return value.get_value(stars=1)
                        else:
                            raise UninitializedVariable(self.interpret(node["name"]) + "." + self.interpret(node['field']),self.current_line)
                    else:
                        return value
                else:
                    return value

            #case struct is used that something is assigned to struct
            if "is_assignment" in node:
                #get variable
                variable = self.current_scope.find_variable(self.interpret(node["name"]),self.interpret(node['field']))
                i=1
                offset=0
                #read offset with position attribute
                if "position" in node:
                    for pos in node['position']:
                        offset= offset + i*self.get_value(self.interpret(pos)) * c_data_types.get(variable.data_type)
                        i += 1
                return [variable, offset]

            else:
                #if struct ist assigned to a variable etc
                variable = self.current_scope.find_variable(self.interpret(node["name"]),self.interpret(node['field']))
                i = 1
                offset = 0
                #read offset with position attribute
                if "position" in node:
                    for pos in node['position']:
                        offset = offset + i * self.get_value(self.interpret(pos)) * c_data_types.get(variable.data_type)
                        i += 1
                stars=0

                #read struct members  from struct pointer
                if node["sub_type"] == "->":
                    stars=1
                #return struct member value
                return RValue(variable.get_value(stars=stars,offset=offset))


        elif node['node_type'] == "ArrayRef":
            #Handle Array references
            if "is_assignment" in node:
                assignment_position=[self.interpret(x) for x in node['position']]
                #if a variable is assigned to an array
                field=None
                if "field" in node:
                    field=self.interpret(node['field'])
                if isinstance(node["name"],str):
                    value= node["name"]
                else:
                    value = self.interpret(node["name"])
                variable = self.current_scope.find_variable(value,field)
                if isinstance(variable.dimension_size,list):
                    for i in range(len(variable.dimension_size)):
                        if variable.dimension_size[i]<=assignment_position[i].get_value():
                            raise MemoryError()
                i=1
                offset=0
                # read offset with position attribute
                for pos in node['position']:

                    offset= offset + i*self.get_value(self.interpret(pos)) * c_data_types.get(variable.data_type)
                    i += 1
                #return variable with offset
                return [variable, offset]

            else:
                variable = self.current_scope.find_variable(node["name"])
                i = 1
                offset = 0
                #get dimension
                if len(node['position']) != variable.dimension:
                    raise WrongArrayDimension(variable.dimension, len(node['position']), self.line)
                # read offset with position attribute
                for pos in node['position']:
                    offset = offset + i * self.get_value(self.interpret(pos)) * c_data_types.get(variable.data_type)
                    i += 1

                #eventually handling array as pointer and vice versa
                if not self.current_scope.is_initialized(variable.address):
                    raise UninitializedVariable(node["name"],self.current_line)
                if not variable.is_array:
                    stars =1
                else:
                    stars = 0
                #Return RValue
                return RValue(variable.get_value(offset=offset,stars=stars))



        elif node["node_type"] == "BinaryOp":
            # Interpretation of binary operation node
            operation = node["operation"]

            # Interpret the left-hand side expression
            lhs = self.interpret(node["lhs"])
            if isinstance(lhs, str):
                lhs = self.current_scope.find_variable(lhs)

            # Interpret the right-hand side expression
            rhs = self.interpret(node["rhs"])
            if isinstance(rhs, str):
                rhs = self.current_scope.find_variable(rhs)

            # Get the values of the left-hand side and right-hand side
            lhs_value = self.get_value(lhs)
            rhs_value = self.get_value(rhs)

            # Convert bytes or bytearrays to integers if necessary
            if isinstance(lhs_value, (bytes, bytearray)):
                lhs_value = ord(lhs_value)
            elif isinstance(rhs_value, (bytes, bytearray)):
                rhs_value = ord(rhs_value)
            # Perform the operation based on the operator
            if operation == "+":
                # Addition
                return RValue(lhs_value + rhs_value)

            elif operation == "-":
                # Subtraction

                return RValue(lhs_value - rhs_value)

            elif operation == "*":
                # Multiplication
                return RValue(lhs_value * rhs_value)

            elif operation == "/":
                # Division
                if isinstance(rhs,float) and str(rhs) == "0.0":
                    return float("inf")
                elif isinstance(rhs, float) and str(rhs) == "-0.0":
                    result = float("-inf")
                elif rhs == 0:
                    raise ZeroDivisionError(self.line)

                elif isinstance(lhs_value, int) and isinstance(rhs_value, int):
                    result = int(lhs_value / rhs_value)
                elif rhs.get_value() == 0.0:
                    result = float("inf")
                else:
                    result = lhs_value / rhs_value

                return RValue(result)

            elif operation == "<=":
                # Less than or equal to comparison
                return lhs_value <= rhs_value

            elif operation == "<":
                # Less than comparison
                return lhs_value < rhs_value

            elif operation == ">=":
                # Greater than or equal to comparison
                return lhs_value >= rhs_value

            elif operation == ">":
                # Greater than comparison
                return lhs_value > rhs_value

            elif operation == "==":
                # Equality comparison
                return lhs_value == rhs_value

            elif operation == "!=":
                # Inequality comparison
                return lhs_value != rhs_value

            else:
                # Unsupported operation
                raise InterpreterError(f"Binary Operation {operation} not implemented", node["line"])


        elif node["node_type"] == "If":
            # Interpretation of if statement node
            if self.interpret(node["cond"]):
                # If the condition is true, interpret the statements within the if block
                value = self.interpret_statements(node['statements'])
                return value

        elif node['node_type'] == "Break":
            # Interpretation of break statement node
            return Value(is_break=True)

        elif node['node_type'] == "Continue":
            # Interpretation of continue statement node
            return Value(is_continue=True)

        elif node['node_type'] == "Return":
            # Interpretation of return statement node
            return Value(is_return=True)

        elif node["node_type"] == "For":
            # Interpretation of for loop node
            # Create a new scope for the loop
            self.current_scope=Scope(self.current_scope)
            statements= node["statements"]
            self.interpret(node["declaration"])

            # Execute the loop until the condition is false
            while self.interpret(node["cond"]):
                # Interpret the statements within the loop body
                value = self.interpret_statements(statements)
                # Interpret the next expression
                self.interpret(node["next"])

                # Handle break, continue, and return statements
                if isinstance(value, Value) and value.is_continue:
                    continue
                elif isinstance(value, Value) and value.is_return:
                    return value
                elif isinstance(value, Value) and value.is_break:
                    # Reset the break flag and exit the loop
                    value.is_break = False
                    break

            # Free memory used by the loop scope and revert to the parent scope
            self.freeMemory(self.current_scope)
            self.current_scope = self.current_scope.parent

        elif node["node_type"] == "While":
            # Interpretation of while loop node
            # Create a new scope for the loop
            self.current_scope = Scope(self.current_scope)
            statements = node["statements"]

            # Execute the loop while the condition is true
            while self.interpret(node["cond"]):
                # Interpret the statements within the loop body
                value = self.interpret_statements(statements)
                # Handle break, continue, and return statements
                if isinstance(value, Value) and value.is_continue:
                    continue
                elif isinstance(value, Value) and value.is_return:
                    return value
                elif isinstance(value, Value) and value.is_break:
                    # Reset the break flag and exit the loop
                    value.is_break = False
                    break

            # Free memory used by the loop scope and revert to the parent scope
            self.freeMemory(self.current_scope)
            self.current_scope = self.current_scope.parent

        elif node["node_type"] == "printf":
            # Interpretation of printf function node
            args=node["args"]

            # Extract the format string from the arguments
            text = args[0].get("value")
            text=text.replace('"','').replace("\\n", "\n")
            replacements=args[1:]
            replacements_formatted=[]

            # Interpret and format the replacement values
            for replacement in replacements:
                value=self.interpret(replacement)

                # Check if the value is a string or variable
                if not isinstance(value,RValue):
                    if isinstance(value,str):
                        value=self.current_scope.find_variable(value)

                    # Check if the variable is initialized
                    if not self.current_scope.is_initialized(value.address):
                        raise UninitializedVariable(node['name'], self.current_line)
                replacements_formatted.append(self.get_value(value))

            # Format the text with the replacements and print it
            text=text % tuple(replacements_formatted)
            print(text)

        elif node["node_type"] == "free":
            # Interpretation of free function node
            args=node["args"]
            value = self.interpret(args[0])
            var = self.current_scope.find_variable(value)
            # Free the memory allocated for the variable
            self.memory.free(var.address)


        elif node["node_type"] == "Assignment":
            # Interpretation of assignment node
            lhs_base = node['lhs']
            lhs_base['is_assignment'] = True

            # Interpret the left-hand side (LHS) of the assignment
            variable = self.interpret(lhs_base)
            if hasattr(variable,"offset"):
                offset = variable.offset
            else:
                offset = 0

            # get offset and variable
            if isinstance(variable,list):
                offset=variable[1]
                variable = variable[0]

            # if variable is LValue find variable in Scope
            if not isinstance(variable,LValue):
                variable = self.current_scope.find_variable(variable)

            # Determine if the variable is an array
            if isinstance(variable,dict):
                is_array=False
            else:
                is_array=variable.is_array

            # Determine stars (pointer levels) and offset for the assignment
            stars=self.get_stars_and_offset(lhs_base,is_array)

            # Handle array assignment
            if isinstance(variable,dict):
                vars = list(variable.values())
                node_rhs = node['rhs']
                do_interpret=True

                # Check if the number of elements in the RHS matches the number of elements in the LHS
                if len(node_rhs) != len(vars):
                    if len(node_rhs) == 1:
                        node_rhs = self.interpret(node_rhs[0])
                        #rhs_start = node_rhs
                        do_interpret=False
                    else:
                        raise WrongArrayDimension(len(vars),len(node_rhs),self.line)

                # Iterate over each element in the RHS and assign it to the corresponding element in the LHS

                for i in range(len(vars)):
                    #if i>0:
                    #    if(split_address(vars[i-1].address)[0]==split_address(vars[i].address)[0]):
                    #        next(i)

                    offset=0
                    key = vars[i]

                    if isinstance(node_rhs,list):
                        value = node_rhs[i]
                    else:
                        value = node_rhs #.get_value(stars=0,offset=offset)


                    # Ensure the value is in list format
                    if not isinstance(value,list):
                        value=[value]

                    # Adjust stars if necessary
                    if not self.current_scope.is_defined(key.data_type) and key.size / get_c_type_size(key.data_type) > 1 and not key.is_pointer:
                        stars = max(stars - 1, 0)

                    # Interpret the RHS values if necessary
                    if do_interpret:
                        for item in value:
                            item["return_value"] = 'lvalue'
                        rhs_start = [self.interpret(x) for x in value]
                    else:
                        rhs_start = [x for x in value]

                    rhs =[]
                    for elem in rhs_start:
                        if isinstance(elem,list):
                            for part in elem:
                                rhs.append(part)
                        else:
                            rhs.append(elem)

                    # Assign each RHS value to the corresponding element in the LHS and determine offset
                    for val in rhs:
                        if isinstance(val, str):
                            val = self.current_scope.find_variable(val)
                        try:
                            if key.is_array and isinstance(val.get_value(),bytes):
                                offset=0
                                while (val.get_value(offset=offset)!=b'\x00'):
                                    key.set_value(val.get_value(offset=offset), self.current_scope, offset=offset, stars=stars)
                                    offset +=1
                            else:
                                key.set_value(val.get_value(), self.current_scope,offset=offset, stars=stars)

                        except ReferenceError as re:
                            raise ReferenceError(f"Variable {variable} could not be dereferenced")

                        #Determine offset
                        if key.data_type in c_data_types:
                            offset = offset + get_c_type_size(key.data_type)

            else:
                # Adjust stars if necessary
                if not self.current_scope.is_defined(variable.data_type) and variable.data_type != "void" and variable.size/get_c_type_size(variable.data_type) >1 and not variable.is_pointer:
                    stars=max(stars-1,0)

                if stars == variable.stars and self.current_scope.is_read_only(variable.address) and self.current_scope.is_initialized(variable.address):
                    raise AssignmentToConstObjectError(variable.get_value(stars=stars),self.line)

                #interpret rhs
                rhs = [self.interpret(x) for x in node['rhs']]

                #loop rhs and assign to lhs
                for val in rhs:
                    if (not hasattr(val,"data_type") or val.data_type is None) or variable.data_type is None:
                        assignment_from_to = ""
                    else:
                        assignment_from_to=val.data_type.replace(" ","") + "_" + variable.data_type.replace(" ","")

                    if assignment_from_to not in valid_assignments and not self.current_scope.is_defined(variable.data_type):
                        raise InvalidConversion(val.data_type,variable.data_type,self.line)
                    if isinstance(val,str):
                        val_str=val
                        val = self.current_scope.find_variable(val)

                        #if not val.is_initialized[int(offset/get_c_type_size(val.data_type))]:
                        if not self.current_scope.is_initialized(val.address):
                            raise UninitializedVariable(val,self.current_line)
                    try:
                        #try to set variable
                        if isinstance(val,Value):
                            if isinstance(val,LValue) and val.is_array and variable.is_pointer:
                                value = val.address
                            else:
                                value = val.get_value()

                            if variable.data_type not in c_data_types and not self.current_scope.is_initialized(value) and val.data_type is not None:
                                raise UninitializedVariable(variable.data_type, self.current_line)

                            #if variable.stars == stars and variable.read_only:
                            #    raise AssignmentToConstObjectError(value, self.__str__)
                            variable.set_value(value, self.current_scope,offset=offset,stars=stars,data_type=variable.data_type)
                        else:
                            variable.set_value(val,self.current_scope)
                    except ReferenceError as re:
                        raise ReferenceError(f"Variable {variable} could not be dereferenced")

                    #determine offset
                    if variable.data_type in c_data_types:
                        offset = offset + get_c_type_size(variable.data_type)

        elif node["node_type"] == "StructDef":
            #Handle Struct Definition
            name = node['name']
            self.current_scope.definitions[name]={"type":"Struct","declaration":node['declarations']}

        elif node['node_type'] == "FuncDef":
            #handle func defintion. Assign Func to current_scope definition
            name = node['name']
            self.current_scope.definitions[name] = {"node_type": "Func", "line": self.line, "name": name,"arguments": node.get('arguments',[]), "statements": node['statements'],"return_type":node['return_type']}

        elif node['node_type'] == "FuncCall":
            #Handle Func Call
            #determine recursion depths
            self.current_recursion_depth += 1

            #abort if recursion depth is to deep
            if self.current_recursion_depth >= self.max_recursion_depth:
                raise MaxRecursionDepthExceededError(self.max_recursion_depth, self.current_line)

            #create new Scope
            self.current_scope = Scope(self.current_scope)


            name = self.interpret(node['name'])

            ##get functin definition and interpret nodes in function
            func_def=self.global_scope.definitions.get(name)

            # get expected args
            expected_args=func_def.get("arguments")

            #get actual args
            actual_args = node.get('args',[])

            #check, taht expcted args=actual args
            self.compareArgs(actual_args,expected_args,name,self.line)

            #interpret args
            for i in range(len(actual_args)):
                self.interpret(expected_args[i])
                name=expected_args[i]['name']
                lhs={"node_type": "ID", "name":name}
                self.interpret({"node_type":"Assignment","lhs": lhs,"rhs":[actual_args[i]]})
            #[self.interpret(actual_args[i])]
            #determine return value
            return_value=self.interpret_statements(func_def['statements'])

            #check if return value is ok and return the value
            if func_def['return_type'] != [] and return_value is not None:
                return_type = " ".join(func_def.get('return_type'))
                if return_type != "void":
                    data_size_return = c_data_types.get(return_type)

                if return_value.data_type != return_type:
                    raise WrongReturnType(return_type,return_value.data_type,self.line)
                self.current_recursion_depth -= 1
                if isinstance(return_value,Value):
                    return_value = return_value.get_value()

            # Free Memory of the scope after function
            self.freeMemory(self.current_scope)
            self.current_scope = self.current_scope.parent

            if func_def['return_type'] != []:
                return return_value

        elif node["node_type"] == "malloc":
            #handle malloc

            #allocate memory
            size = self.interpret(node["args"][0])

            address = self.memory.malloc(size.get_value())
            return RValue(address)

        else:
            raise Exception("AST not implemented")

    def get_stars_and_offset(self,node,is_array=False):
        """
                Determine the number of stars and offset for a given AST node.

                Parameters:
                    node: The AST node.
                    is_array (bool): Indicates if the node represents an array.

                Returns:
                    int: The number of stars.
        """
        expression = node
        node_type = expression['node_type']
        if "operation" in expression:
            operation = expression['operation']
        stars=0

        while "expression" in expression.keys() and node_type=="UnaryOp" and operation == "*":
            node_type = expression['node_type']
            operation = expression['operation']
            expression = expression['expression']
            stars = stars +1

        if not is_array and "position" in expression:
            stars += 1
        if "sub_type" in expression:
            if expression["sub_type"]== "->":
                stars = stars + 1

        return stars

    def get_value(self,expression):
        """
            Get the value from an expression.

            Parameters:
                expression: The expression to get the value from.

            Returns:
                Value: The value of the expression.
        """
        if isinstance(expression,RValue):
            return expression.get_value()
        elif isinstance(expression,LValue):
            return expression.get_value()
        elif isinstance(expression,str):
            return self.get_value(self.current_scope.find_variable(expression))
        else:
            return expression

    def interpret_statements(self, statements):
        """
                Interpret a list of statements.

                Parameters:
                    statements (list): The list of statements to interpret.

                Returns:
                    None
        """
        for statement in statements:
            value = self.interpret(statement)
            if isinstance(value, Value) and value.is_break:
                return value
            elif isinstance(value, Value) and value.is_continue:
                #doBreak = True
                return value
            elif isinstance(value, Value) and value.is_return:
                return value

    def interpret_function_call(self, node: c_ast.FuncDef, current_scope: Scope) -> Optional[Value]:
        """
                Interpret a function call.

                Parameters:
                    node (c_ast.FuncDef): The function definition node.
                    current_scope (Scope): The current scope.

                Returns:
                    Optional[Value]: The result of the function call.
        """
        func_name = node.decl.name
        func_type = node.decl.type

        function_scope = Scope(current_scope)

        function_scope.parent.variables[func_name] = None

        return_value = self.interpret_statements(node.body, function_scope)

        if return_value is not None and return_value.is_return:
            return return_value

    def compareArgs(self, expectedArgs,actualArgs,method_name,line):
        """
                Compare expected and actual arguments in a function call.

                Parameters:
                    expectedArgs: The expected arguments.
                    actualArgs: The actual arguments.
                    method_name: The name of the method being called.
                    line: The line number of the method call.

                Returns:
                    bool: True if arguments match, False otherwise.
        """
        if len(expectedArgs) != len(actualArgs):
            raise WrongNumberOfArguments(len(expectedArgs),len(actualArgs),method_name,self.line)
        #else:
        #    for i in range(len(expectedArgs)):
        #        if expectedArgs[i]['data_type']!=actualArgs[i]['data_type']:
        #            raise WrongDataType(expectedArgs[i]['data_type'],actualArgs['data_type'],self.line)

        return True

    def ast_to_json(self, node: c_ast.Node):
        """
                Convert AST nodes to JSON format.

                Parameters:
                    node (c_ast.Node): The AST node to convert.

                Returns:
                    dict: The JSON representation of the AST node.
        """
        if isinstance(node, c_ast.Node):
            return {type(node).__name__: {key: self.ast_to_json(value) for key, value in node.children()}}

        return node

    def run(self, parsed_code: list[dict],freeScope=True) -> Optional[Value]:
        """
                Run the interpreter on parsed code.

                Parameters:
                    parsed_code (list): The parsed code in AST format.
                    freeScope (bool): Flag to free scope after execution.

                Returns:
                    Optional[Value]: The result of execution.
        """
        for node in parsed_code:
            #self.interpret(node,self.global_scope)
            self.interpret(self.ast_to_json(node))
        if "main" in self.global_scope.definitions:
            callable_func={'node_type': 'FuncCall', "line":0, 'name': {'node_type': 'ID', 'line': 0, 'name': 'main'}}
            self.interpret(callable_func)
        if freeScope:
            self.freeMemory(self.global_scope)