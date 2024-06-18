from typing import List, Dict, Tuple, Optional
import secrets

def split_address(address: int) -> Tuple[int, int]:
    """
        Splits a memory address into base address and offset.

        Args:
            address (int): The memory address.

        Returns:
            Tuple[int, int]: A tuple containing the base address and offset.
    """
    # Base address is upper 128 bits
    base_address = address & 0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_00000000
    # Offset is lower 64 bits
    offset = address & 0xFFFFFFFF_FFFFFFFF
    return base_address, offset



class Memory:
    def __init__(self,random_bits_size=128) -> None:
        """
                Initializes the Memory class.

                Args:
                    random_bits_size (int): The size of random bits used for address generation.
        """
        # Stores all memory allocations indexed by memory address
        self.allocations: Dict[int, Optional[bytearray]] = {}
        self.byteorder = "little"
        self.random_bits_size=random_bits_size
    #

    def malloc(self, size:int,sibling_address:int = 0) -> int:
        """
                Allocates memory and returns the base address.

                Args:
                    size (int): The size of memory to allocate.

                Returns:
                    int: The base address of the allocated memory.
        """

        assert size <= 2**64, f"Can not allocate more than 2**64 bytes, but tried to allocate {size} bytes"
        if sibling_address==0:
            random_bits = secrets.randbits(self.random_bits_size)
            base_address = random_bits << 64
        else:
            base_address = sibling_address

        xtra_byte =bytearray()
        if base_address in self.allocations:
            xtra_byte=self.allocations[base_address]
        # Allocate bytes
        self.allocations[base_address] = xtra_byte + bytearray(size)#

        return base_address



    def free(self, address: int) -> None:
        """
               Frees the allocated memory at the given address.

               Args:
                   address (int): The base address of the allocated memory.
        """
        #base_address,offset=split_address(address)
        #if base_address in self.allocations:
        #    self.allocations[base_address] = None
        #    return
        if address not in self.allocations:
            raise MemoryError(f"Can not free address {hex(address)} because it has never been allocated")

        if self.allocations[address] is None:
            raise MemoryError(f"Double-free of address {hex(address)}")

        self.allocations[address] = None

    def read(self, address: int, size: int,ignore_offset=False) -> bytes:
        """
                Reads data from the allocated memory.

                Args:
                    address (int): The memory address to read from.
                    size (int): The size of data to read.

                Returns:
                    bytes: The read data.
        """
        base_address, offset = split_address(address)
        if ignore_offset:
            offset=0
        # Ist die Basisadresse nicht im Dictionary (self.allocations) enthalten...
        if base_address not in self.allocations:
            # ... dann wird die adresse gesucht, die am nächsten an der Adresse liegt
            closest_allocation = min(self.allocations, key=lambda x: abs(x - base_address))
            # ... und ein Fehler ausgegeben mit Ausgabe der nächstgelegenen Adresse
            raise MemoryError(f"Invalid read of size {size} at {hex(address)} - No allocation found. Closest allocation is at {hex(closest_allocation)}")


        allocation = self.allocations[base_address]

        if allocation is None:
            raise MemoryError(f"Invalid read of size {size} at {hex(address)} - memory has been freed already")

        if offset + size > len(allocation):
            raise MemoryError(f"Invalid read of size {size} at {hex(address)}")

        return bytes(allocation[offset : offset + size])

    def write(self, address: int, data: bytes) -> None:
        """
                Writes data to the allocated memory.

                Args:
                    address (int): The memory address to write to.
                    data (bytes): The data to write.
        """
        base_address, offset = split_address(address)
        size = len(data)

        if base_address not in self.allocations:
            raise MemoryError(f"Invalid write of size {size} at {hex(address)}")

        allocation = self.allocations[base_address]

        if allocation is None:
            raise MemoryError(f"Invalid write of size {size} at {hex(address)} - memory has been freed already")

        if offset + size > len(allocation):
            raise MemoryError(f"Invalid write of size {size} at {hex(address)}")

        allocation[offset : offset + size] = data