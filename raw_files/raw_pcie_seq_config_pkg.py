#class cfg_type(IntEnum):
#   type0 =0
#   type1 =1

import random 
from pprint import pprint

from enum import IntEnum
from bitstring import BitArray

class pcie_pkg:
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        with open("bdf_file.txt","w") as f:
            f.write("bdf")
            self.transaction_type = random.getrandbits(8)
            self.bdf = random.getrandbits(16)
            self.cfg_type = random.getrandbits(1)
            self.first_dw_be = 0b0011
            self.ep = random.getrandbits(1)
            self.block = random.getrandbits(1)
            self.td= random.getrandbits(1)
            #self.header= {} 
            #self.payload= random.getrandbits(1)
            #self.ecrc= random.getrandbits(1)
            #self.command_num = random.getrandbits(32)
            ############### code for byte conv #############
            self.name = name
            self.size_in_bytes = size_in_bytes
            self.xwr = xwr
            ################################################
            f.write(hex(self.bdf))
            f.write("\n")
    

    def print_var(self):
        pprint(vars(self))
        '''s = bin(self.first_dw_be)
        pprint(s)
        a = 20
        print(bytes(a))
        b=BitArray(uint = a , length = 10).bin
        pprint(b)
        for i in range(1,11): 
            pprint(b[i-1:i])
'''
    def bitwise_read():
        s = bin(self.first_dw_be)
        pprint(s)
        a = 20
        print(bytes(a))
        b=BitArray(uint = a , length = 10).bin
        pprint(b)
        for i in range(1,11): 
            pprint(b[i-1:i])
    
 
class tlp_fmt(IntEnum):
    cfgrd=0b000
    cfgwr=0b010

class tlp_type(IntEnum):
    cfgwr0=0b0001
    cfgrd0=0b0010
    cfgwr1=0b0011
    cfgrd1=0b0100


pkg = pcie_pkg()
pkg.print_var()




