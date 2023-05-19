import random
from pcie_com_file import *
from pcie_ep_com_file import *

from tabulate import tabulate

print("ep_memory_space block")



MEMORY_SIZE = (1024*8)/32  # 1KB - Total number of memory locations
Address_RANGE_START = 0  # Start Address of the desired range
Address_RANGE_END = 255  # End Address of the desired range
memory = {}
mem= open('memory_contents.txt', 'w')
'''def print_memory():
        for Address, Data in memory.items():
            print(f"Address: {hex(Address)}, Data: {hex(Data)}")'''


def def_write(Address, Data):
    if Address < 0 or Address >= MEMORY_SIZE:
        mem.write(f"Error: Address {hex(Address)} is out of bounds.")
        return
    if Address < Address_RANGE_START or Address > Address_RANGE_END:
        mem.write(f"Warning: Address {hex(Address)} is outside the desired range. Range must be between 00 - ff. Ignoring Data.")
        return
    # Split the Data into 32-bit chunks
    chunks = [(Data >> i) & 0xFFFFFFFF for i in range(0, 1024 * 8, 32)]  # 1024 bytes = 8KB = 256(locations) * 32bit Data

    # Calculate the number of chunks to write based on the available memory size
    num_chunks_to_write = min(len(chunks), (Address_RANGE_END - Address + 1) // 4)

    # Store the chunks in consecutive Addresses within the desired range
    for i, chunk in enumerate(chunks[:num_chunks_to_write]):
        memory[Address + (i * 4)] = chunk

def_write(int(hex(0), 16), int(hex(random.getrandbits(1024*8)), 16))
#print_memory()


table_Data = []
class pcie_ep_memory_space:

    def write_request(pkt_num, Address, Data):
        def_write(Address, Data)
        
        for Address, Data in memory.items():
            table_Data.append([hex(Address), hex(Data)])
        table = tabulate(table_Data, headers=["Address", "Data"], tablefmt="grid")
        mem.write('\n\n printing memory write request packet {} \n\n' '{}\n'.format(pkt_num,table))
            
    def read_request(pkt_num, Address):
        for Address, Data in memory.items():
            table_Data.append([hex(Address), hex(Data)])
        table = tabulate(table_Data, headers=["Address", "Data"], tablefmt="grid")
        mem.write('\n\n printing memory read request packet {} \n\n' '{}\n'.format(pkt_num,table))

        if Address in memory:
            return format(memory[Address], '032b')
        else:
            return None

        
            

# Create an instance of the Memory class
#mem = pcie_ep_memory_space()

# Write a 64-bit value to Address 0x100

#mem.write(0x1000, int(hex(random.getrandbits(4096*8)), 16))
#mem.print_memory()
# Read the value from Address 0x100
#Data = mem.read(0x1000)

#print(hex(Data))  # Output: 0x90abcdef

# Read the value from Address 0x101 (next Address)
#Data = mem.read(0x1001)

#print(hex(Data))  # Output: 0x1234567

# Define the file name

    # Prepare the table Data
    


