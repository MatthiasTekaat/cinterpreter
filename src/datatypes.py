class DataTypeError(Exception):
    def __init__(self, data_type: str, line: int = 0) -> None:
        """
             Exception-Klasse for Data Type errors

            Args:
                data_type (str): not valid data type
                line (int): line number of error
        """
        super().__init__("{} is not a valid data type. Datatype must be of {}".format(data_type, c_data_types.keys()), line)

#Dictionary of data types mapped to byte size
c_data_types = {
    'char': 1,
    'unsigned char': 1,
    'short': 2,
    'unsigned short': 2,
    'int': 4,
    'unsigned int': 4,
    'long': 4,
    'unsigned long': 4,
    'long long': 8,
    'unsigned long long': 8,
    'float': 4,
    'double': 8,
    'size_t': 8,
    'void': 0
}

def get_c_type_size(c_type_str) -> int:
    """
        Gibt die Größe des angegebenen C-Datentyps zurück.

        Args:
            c_type_str (str): Der C-Datentyp als Zeichenkette.

        Returns:
            int: Die Größe des C-Datentyps in Bytes.

        Raises:
            DataTypeError: Wenn der angegebene C-Datentyp ungültig ist.
    """
    if c_type_str in c_data_types.keys():
        return c_data_types.get(c_type_str)
    else:
        raise DataTypeError(c_type_str)