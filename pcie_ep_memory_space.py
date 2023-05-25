import random
from pcie_com_file import *
from pcie_ep_com_file import *

from tabulate import tabulate

print("ep_memory_space block")

MEMORY_SIZE = 64 * 32  # 256B - Total number of memory locations is 64  ---> 64*32=2048 bits--->2048 % 8 byte=256B
Address_RANGE_START = 0  # Start Address of the desired range
Address_RANGE_END = 63  # End Address of the desired range
memory = {}
mem = open('ep_logs/memory_contents.txt', 'w')

def print_memory(type_i, pkt_num):
    table_data = []
    for Address, Data in memory.items():
        table_data.append([hex(Address), hex(Data)])
    table = tabulate(table_data, headers=["Address", "Data"], tablefmt="grid")
    mem.write(f"\n Memory contents for {type_i} packet {pkt_num}:\n")
    mem.write(table)

'''def def_write(Addr, data_rec):
    if Addr < Address_RANGE_START or Addr > Address_RANGE_END:
        mem.write(f"\nError: Address {hex(Addr)} is outside the desired range. Range must be between 0x00 - 0x40. Ignoring Data.\n")
        return 0

    memory[Addr] = data_rec & 0xFFFFFFFF  # Store the lower 32 bits at the given address'''

def get_data_chunk(data_rec, start_bit, num_bits):
    mask = (1 << num_bits) - 1
    return (data_rec >> start_bit) & mask

def write_data_to_memory(start_address, data_rec):
    num_bits = len(bin(data_rec)[2:])  # Get the number of bits in the data #removing the prefix '0b' with [2:], and calculating the length of the resulting string.
    num_chunks = (num_bits + 31) // 32   # It adds 31 to num_bits to ensure that any remainder is rounded up to the nearest multiple of 32, and then performs integer division by 32.

    for i in range(num_chunks):
        if start_address + i > Address_RANGE_END:
            break
        chunk = get_data_chunk(data_rec, i * 32, 32)
        memory[start_address + i] = chunk                # start_address + 1  is used for allignment of address if we are geting data more then 32

write_data_to_memory(int(hex(0), 16), int(hex(random.getrandbits(64*32)), 16))
print_memory('DEFAULT', 0)


class pcie_ep_memory_space:
    def write_request(pkt_num, Addr, data_rec):
        if Addr < Address_RANGE_START or Addr > Address_RANGE_END:
            mem.write(f'\n *******************  packet {pkt_num} ***************** \n')
            mem.write(f"\n Error: For Write Request, Address {hex(Addr)} is outside the desired range. Range must be between 0x00 - 0x40. Ignoring Data.\n")
            return 0
        else:
            write_data_to_memory(Addr, data_rec)
            mem.write(f'\n *******************  packet {pkt_num} ***************** \n')
            mem.write(f'\n Write request at Address {hex(Addr)}, data is {hex(data_rec)}\n')
            print_memory('write', pkt_num)
        
    def read_request(pkt_num, Addr):
        if ((Addr < Address_RANGE_START) or (Addr > Address_RANGE_END)):
            mem.write(f'\n *******************  packet {pkt_num} ***************** \n')
            mem.write(f"\n Error: For Read Request, Address {hex(Addr)} is outside the desired range. Range must be between 0x00 - 0x40. Ignoring Data.\n")
            return 0
        else:
            if Addr in memory:
                mem.write(f'\n *******************  packet {pkt_num} ***************** \n')
                mem.write(f'Read request at Address {hex(Addr)}, data is {hex(memory[Addr])}\n')
                print_memory('Read', pkt_num)
                return format(memory[Addr], '032b')
            else:
                mem.write('returning 0 from mem space')
                return 0

        
            
    


