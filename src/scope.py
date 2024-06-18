from typing import Dict, Optional

from numpy.core._dtype import __str__

#from value import Value

from errorhandler import UndefinedVariable,UninitializedVariable


class Scope:
    def __init__(self, parent: Optional["Scope"] = None):
        """
                Initializes a new Scope.

                Args:
                    parent (Optional[Scope]): The parent scope. Defaults to None.
        """
        # Constructor Initializes a new Scope.
        # A scope can have a parent Scope
        self.parent = parent
        # "variables" is a Dictionary, storing variables of current scope
        self.variables = {} #: dict[str, Value]
        self.definitions:dict[str,dict]={}
        self.initialisations: set = set([])
        self.read_onlys: set = set([])



    def get_scope(self, data_type) -> dict:
        """
                        Finds if a own data_type was defined within a scope

                        Args:
                            address (int): Address to find

                        Returns:
                            bool: True if varaible initialized in Scope, otherwise false
        """

        # The method "find_variable" searches for a variable with the specified name in the current scope.
        if data_type in self.definitions:
            return self.definitions
        elif self.parent:
            # If the variable is not found in the current scope, the search extends to the (parent) scope.
            return self.parent.get_scope(data_type)
        else:
            return None

    def is_defined(self, data_type) -> bool:
        """
                        Finds if a own data_type was defined within a scope

                        Args:
                            address (int): Address to find

                        Returns:
                            bool: True if varaible initialized in Scope, otherwise false
        """

        # The method "find_variable" searches for a variable with the specified name in the current scope.
        if data_type in self.definitions:
            return True
        elif self.parent:
            # If the variable is not found in the current scope, the search extends to the (parent) scope.
            return self.parent.is_defined(data_type)
        else:
            return False

    def add_read_onlys(self,address):
        """
                    Adds an address to be read_only within a scope

                    Args:
                        address (int): Address to add
        """
        self.read_onlys.add(address)

    def is_read_only(self, address) -> bool:
        """
                        Finds if a address is read_only within a scope

                        Args:
                            address (int): Address to find

                        Returns:
                            bool: True if varaible is read_only in Scope, otherwise false
        """

        # The method "find_variable" searches for a variable with the specified name in the current scope.
        if address in self.read_onlys:
            return True
        elif self.parent:
            # If the variable is not found in the current scope, the search extends to the (parent) scope.
            return self.parent.is_read_only(address)
        else:
            return False
            # If the variable is not found in the current scope or any parent scopes,
            # "None" is returned to indicate that the variable is not defined.
            #raise UninitializedVariable(address)

    def add_initialisation(self,address):
        """
                    Adds an address to be initialized within a scope

                    Args:
                        address (int): Address to add
        """
        self.initialisations.add(address)


    def is_initialized(self, address) -> bool:
        """
                        Finds if a address was initialized within a scope

                        Args:
                            address (int): Address to find

                        Returns:
                            bool: True if varaible initialized in Scope, otherwise false
        """

        # The method "find_variable" searches for a variable with the specified name in the current scope.
        if address in self.initialisations:
            return True
        elif self.parent:
            # If the variable is not found in the current scope, the search extends to the (parent) scope.
            return self.parent.is_initialized(address)
        else:
            return False
            # If the variable is not found in the current scope or any parent scopes,
            # "None" is returned to indicate that the variable is not defined.
            #raise UninitializedVariable(address)


    def find_variable(self, name: str,child:str = None) -> list:
        """
                Finds a variable with the specified name in the current scope or its parent scopes.

                Args:
                    name (str): The name of the variable to find.
                    child (Optional[str]): The child variable name (if it's a nested variable). Defaults to None.

                Returns:
                    Optional[Value]: The found variable value if exists, otherwise raises UndefinedVariable.
        """

        # The method "find_variable" searches for a variable with the specified name in the current scope.
        if name in self.variables:
            # If the variable is found in the current scope, it is returned.
            if child is None:
                return self.variables[name]
            else:
                if child in self.variables[name]:
                    return self.variables[name].get(child)
                else:
                    raise UndefinedVariable(f"{name}.{child}")
        elif self.parent:
            # If the variable is not found in the current scope, the search extends to the (parent) scope.
            if child is None:
                return self.parent.find_variable(name)
            else:
                return self.parent.find_variable(name,child)

        else:
            # If the variable is not found in the current scope or any parent scopes,
            # "None" is returned to indicate that the variable is not defined.
            raise UndefinedVariable(name)

    __repr__ = __str__
