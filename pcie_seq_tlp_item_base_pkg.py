#class cfg_type(IntEnum):
#   type0 =0
#   type1 =1

import random 
from pprint import pprint

from enum import IntEnum
#from bitarray import bitarray

class pcie_pkg:
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        with open("bdf_file.txt","w") as f:
            f.write("bdf")
            self.fmt = random.getrandbits(3)	
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
            f.write(hex(self.bdf))
            f.write("\n")
    
    
 
class tlp_fmt(IntEnum):
    cfgrd=0b000
    cfgwr=0b010

class tlp_type(IntEnum):
    cfgwr0=0b0001
    cfgrd0=0b0010
    cfgwr1=0b0011
    cfgrd1=0b0100


pkg = pcie_pkg()





