import random
from pcie_com_file import *
from pcie_ep_com_file import *

from tabulate import tabulate

print("ep_memory_space block")

memory = {}
mem= open('memory_contents.txt', 'w')
'''def print_memory():
        for Address, Data in memory.items():
            print(f"Address: {hex(Address)}, Data: {hex(Data)}")'''


def def_write(Address, Data):
        # Split the Data into 32-bit chunks
        chunks = [(Data >> i) & 0xFFFFFFFF for i in range(0, 1024*8, 32)]    # 4KB = 4096(locations) * 8bit Data 

        # Store the chunks in consecutive Addresses
        for i, chunk in enumerate(chunks):
            memory[Address + i] = chunk

def_write(int(hex(random.getrandbits(29)), 16), int(hex(random.getrandbits(1024*8)), 16))
#print_memory()


table_Data = []
class pcie_ep_memory_space:

    def write_request(pkt_num, Address, Data):
        # Split the Data into 32-bit chunks
        chunks = [(Data >> i) & 0xFFFFFFFF for i in range(0, 1024*8, 32)]    # 4KB = 4096(locations) * 8bit Data 

        # Store the chunks in consecutive Addresses
        for i, chunk in enumerate(chunks):
            memory[Address + i] = chunk
        
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
            return memory[Address]
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
    


