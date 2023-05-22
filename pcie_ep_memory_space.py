import random
from pcie_com_file import *
from pcie_ep_com_file import *

from tabulate import tabulate

print("ep_memory_space block")

MEMORY_SIZE = (256 * 8) // 32  # 1KB - Total number of memory locations
Address_RANGE_START = 0  # Start Address of the desired range
Address_RANGE_END = 63  # End Address of the desired range
memory = {}
mem = open('ep_logs/memory_contents.txt', 'w')

def print_memory(type_i, pkt_num):
    table_data = []
    for Address, Data in memory.items():
        table_data.append([hex(Address), hex(Data)])
    table = tabulate(table_data, headers=["Address", "Data"], tablefmt="grid")
    mem.write('\n\n printing memory {} request packet {} \n\n' '{}\n'.format(type_i, pkt_num,table))

def def_write(Addr, data_rec):
    
    if Addr < Address_RANGE_START or Addr > Address_RANGE_END:
        mem.write(f"\nError: Address {hex(Addr)} is outside the desired range. Range must be between 00 - ff. Ignoring Data.\n")
        return
    
    chunks = [(data_rec >> i) & 0xFFFFFFFF for i in range(0, 256 * 8, 32)]  # 1024 bytes = 8KB = 256(locations) * 32bit Data

    
    num_chunks_to_write = min(len(chunks), (Address_RANGE_END - Addr + 1) // 4)

    
    for i, chunk in enumerate(chunks[:num_chunks_to_write]):
        memory[Addr + (i * 4)] = chunk

def_write(int(hex(0), 16), int(hex(random.getrandbits(256*8)), 16))



class pcie_ep_memory_space:

    def write_request(pkt_num, Addr, data_rec):
        if Addr < Address_RANGE_START or Addr > Address_RANGE_END:
            mem.write(f"\nError: Address {hex(Addr)} is outside the desired range. Range must be between 00 - ff. Ignoring Data.\n")
            return
        else:
            def_write(Addr, data_rec)
            mem.write('write data packet {} from Address {} , data is {}'.format(pkt_num, Addr, hex(data_rec)))
            print_memory('write', pkt_num)
        #print_memory()
        
            
    def read_request(pkt_num, Addr):
        if Addr < Address_RANGE_START or Addr > Address_RANGE_END:
            mem.write(f"\nError: Address {hex(Addr)} is outside the desired range. Range must be between 00 - ff. Ignoring Data.\n")
            return

        if Addr in memory:
            mem.write('read data packet {} from Address {} , data is {}'.format(pkt_num, Addr, hex(memory[Addr])))
            print_memory('read', pkt_num)
            return format(memory[Addr], '032b')
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
    


