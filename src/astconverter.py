
from pycparser import c_ast

'''
The AstConverter class facilitates the conversion of a C code Abstract Syntax Tree (AST) 
into a comprehensible and hierarchically structured dictionary. This dictionary can 
then be further used to represent the AST in a different format or to extract specific 
information from the code.
'''

def flatten(lst):
    """
        Flattens a nested list.

        Args:
            lst (list): The nested list.

        Returns:
            list: The flattened list.
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

class AstConverter:

    def __init__(self,code):
        """
        Initializes an AstConverter.

        Args:
            code (str): The code to be converted.
        """
        self.parsed_code=code
        self.code_dict=[]

    def convert_node(self,node):
        """
        Converts an AST node into a dictionary.

        Args:
            node (c_ast.Node): The AST node to be converted.

        Returns:
            dict: The converted dictionary.
        """
        if isinstance(node, c_ast.Node):
            node_type=node.__class__.__name__
            result = {'node_type': node_type, 'line': f"{node.coord.line}:{node.coord.column}"}#, 'data_type': node.type.type.names}

            #Abhandlung der Verschiedenen Node_Types
            if node_type == 'FuncDef':
                # Processing Function Definition
                result['name'] = node.decl.name
                result['return_type']= node.decl.type.type.type.names

                # Check if function has arguments
                if node.decl.type.args is not None:
                    result['arguments'] = [self.convert_node(item) for item in node.decl.type.args]
                # Process statements within the function
                if node.body.block_items is not None:
                    result['statements']=[self.convert_node(item) for item in node.body.block_items]
                else:
                    result['statements'] = []
            elif node_type == 'InitList':
                # Processing Initialization List
                return [self.convert_node(x) for x in node.exprs]
            elif node_type == 'Cast':
                # Processing Type Casting
                result['expression']=self.convert_node(node.expr)
                result['to_type'] = self.convert_node(node.to_type)

            elif node_type == 'Decl':
                # Processing Variable Declaration
                if node.name is not None:

                    result['name']= node.name
                    result['rights'] = " ".join(node.quals)
                    # Special handling for Pointers
                    if node.type.__class__.__name__=='PtrDecl':
                        # Count the number of pointer stars
                        stars = 0
                        tryIt = True
                        #tryString = "node.type.type"

                        tryString = "node.type.type"
                        while tryIt == True:
                            try:
                                result['data_type'] = " ".join(eval(tryString + ".names"))  # node.type.type.type.names[0]
                                tryIt = False
                            except:
                                try:
                                    result['data_type'] = eval(tryString + ".name")  # node.type.type.type.names[0]
                                    tryIt = False
                                except:
                                    stars += 1
                                    tryString += ".type"

                        if result['data_type'] == 'char':
                            result['rights'] = "const"

                        result['stars'] = stars
                        result['node_type'] = node_type
                        # Check for initialization and create Assignment statement
                        if node.init is not None:
                            rhs = self.convert_node(node.init)
                            if not isinstance(rhs, list):
                                rhs = [rhs]
                            result['statements'] = [{'node_type': 'Assignment',
                                                     'lhs': {"node_type": "ID", "name": node.name},
                                                     'rhs': rhs}]
                    # Processing Type Declaration
                    elif node.type.__class__.__name__=='TypeDecl':
                        type_info=node.type.type
                        # Check for initialization and create Assignment statement
                        if hasattr(type_info,"names"):
                            result['data_type'] = " ".join(node.type.type.names)
                        else:
                            result['data_type'] = node.type.type.name
                        result['stars'] = 0
                        if node.init is not None:
                            rhs = self.convert_node(node.init)
                            if not isinstance(rhs,list):
                                rhs=[rhs]
                            result['statements']=[{'node_type': 'Assignment',
                                                   'lhs': {"node_type": "ID", "name" : node.name},
                                                   'rhs': rhs}]
                    # Processing Array Declaration
                    elif node.type.__class__.__name__=='ArrayDecl':
                        node_type = node
                        result['is_array']=True
                        result['dimension']=[]
                        result['stars'] = 0

                        # Extract dimension information
                        while hasattr(node_type, 'type'):
                            node_type = node_type.type
                            if hasattr(node_type, 'dim') and node_type.dim is not None:
                                result['dimension'].append(self.convert_node(node_type.dim)['value'])

                        if hasattr(node_type,"names"):
                            result['data_type'] = " ".join(node_type.names)
                        else:
                            result['data_type'] = node_type.name
                        #result['data_type'] = node_type.names[0]

                        # Check for initialization and create Assignment statements
                        if node.init is not None:
                            rhs = []
                            for x in node.init:
                                interpreted_value=self.convert_node(x)
                                if isinstance(interpreted_value,list):
                                    rhs.extend(interpreted_value)
                                else:
                                    rhs.append(interpreted_value)
                            result['statements'] = [{'node_type': 'Assignment',
                                                     'lhs': {"node_type": "ID", "name": node.name},
                                                     'rhs': [self.convert_node(x) for x in rhs]}]

                else:
                    # Processing Struct Definition
                    result = {'node_type': "StructDef"}
                    result['name'] = node.type.name
                    result['declarations'] = [self.convert_node(item) for item in node.type.decls]

            elif node_type == 'ID':
                # Processing Identifier
                result['name'] = node.name

            elif node_type == 'Typename':
                # Processing Type Name
                current_level = node.type.type
                stars=0

                # Count the number of pointer stars
                while hasattr(current_level,"type"):
                    stars +=1
                    current_level=current_level.type
                result['stars'] = stars
                if hasattr(current_level,"names"):
                    result['name'] = current_level.names[0]
                else:
                    result['name'] = current_level.name

            elif node_type == 'Constant':
                result['data_type'] = node.type
                if node.type not in ['string']:
                    if node.value[-1]=='f':
                        node.value=node.value[:-1]
                    result['value']= eval(node.value)
                else:
                    result['value'] = node.value.replace('"','')

            elif node_type == 'Assignment':
                # Process Assignment Statement
                result['lhs'] = self.convert_node(node.lvalue)
                result['operation'] = self.convert_node(node.op)
                result['rhs'] = [self.convert_node(node.rvalue)]

            elif node_type == 'Return':
                # Process Return Statement
                result['value']= self.convert_node(node.expr)

            elif node_type == 'BinaryOp':
                # Process Binary Operation
                result['lhs'] = self.convert_node(node.left)
                result['rhs'] = self.convert_node(node.right)
                result['operation'] = self.convert_node(node.op)

            elif node_type == 'UnaryOp':
                # Process Unary Operation
                result['expression'] = self.convert_node(node.expr)
                result['operation'] = self.convert_node(node.op)

            elif node_type == 'FuncCall':
                # Process Function Call
                result['name'] = self.convert_node(node.name)
                # Handle specific functions separately
                # As malloc is allocation memory, which uses special python function,
                # we need a special treatment
                if node.name.name == "malloc":
                    result['node_type'] = "malloc"
                elif node.name.name == "printf":
                    result['node_type'] = "printf"
                elif node.name.name == "sizeof":
                    result['node_type'] = "sizeof"
                elif node.name.name == "free":
                    result['node_type'] = "free"

                result['args'] = [self.convert_node(item) for item in node.args]

            elif node_type == 'While':
                # Process While Loop
                result['cond'] = self.convert_node(node.cond)
                result['statements'] = [self.convert_node(item) for item in node.stmt.block_items]

            elif node_type == 'For':
                # Process For Loop
                result['cond'] = self.convert_node(node.cond)
                result['declaration'] = self.convert_node(node.init.decls[0])
                result['next'] = self.convert_node(node.next)
                result['statements'] = [self.convert_node(item) for item in node.stmt.block_items]

            elif node_type == 'If':
                # Process If Statement
                result['cond'] = self.convert_node(node.cond)
                result['statements'] = [self.convert_node(item) for item in node.iftrue.block_items]

            elif node_type == 'ArrayRef':
                # Process Array Reference
                result['position'] = []
                result['position'].insert(0,self.convert_node(node.subscript))
                current_node = node.name
                while hasattr(current_node,"subscript"):
                    result['position'].insert(0,self.convert_node(current_node.subscript))
                    current_node = current_node.name
                result['name']=self.convert_node(current_node.name)
                if hasattr(current_node,"field"):
                    result['field'] = self.convert_node(current_node.field)

            elif node_type == 'StructRef':
                # Process Struct Reference
                current_node = node
                result['name']= self.convert_node(current_node.name)
                result['field'] = self.convert_node(current_node.field)
                result['sub_type'] = current_node.type

            elif node_type == 'Continue' or node_type == 'Break':
                # Continue and Break statements, no additional information needed
                #only shown here, that it is recognized as handled node type
                1==1

            else:
                # Raise exception for unimplemented node types
                raise Exception(f"Node Type Conversion for node type {node_type} not implemented")

            return result
        # if lis of node types proces each node in list
        elif isinstance(node, list):
            return [self.convert_node(item) for item in node]

        else:
            return node

    def ast_to_dict(self):
        """
                Converts the entire AST to a list of dictionaries.
        """
        for node in self.parsed_code.ext:
            self.code_dict.append(self.convert_node(node))