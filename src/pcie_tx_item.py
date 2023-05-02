#class pcie_tx_item:
#    print("2. This is pcie_tx_item class")
#    def __init__(self):
#      self.fmt=0
#      self.bdf = 0b1011    
#class cfg_type(IntEnum):
#   type0 =0
#   type1 =1

import random 
from pprint import pprint

from enum import IntEnum

#class pcie_pkg:
class pcie_tx_item:
    print("2. This is pcie_tx_item class")
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        self.transaction_type = random.getrandbits(8)	
        self.bdf = 10
        self.conf_type = 0
        self.first_dw_be = 0b0011
        self.ep = 0
        self.block = random.getrandbits(1)
        self.td = 0
        #self.command_num = random.getrandbits(32)
        ############### code for byte conv #############
        self.name = name
        self.size_in_bytes = size_in_bytes
        self.xwr = xwr
        ################################################
    

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


pkg = pcie_tx_item()
pkg.print_var()
