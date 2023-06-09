from pcie_lib import *
import random 
from enum import IntEnum
from pcie_com_file import *
logger.info(f"{formatted_datetime} \t\tROOT COMPLEX : Compiling pcie_seq_tlp_item_base_pkg.py file")

class pcie_pkg:
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        self.fmt                    = 0
        ##    BDF format for requester and completer    ##
        self.requester_id           = 0
        self.completer_id           = 0
        ##############################
        self.type                   = 0
        self.first_dw_be            = 0
        self.ep                     = 0 
        self.td                     = 0
        self.tc                     = 0
        self.attr0                  = 0
        self.attr1                  = 0
        self.at                     = 0
        self.length                 = 0

        #self.bus                    =0
        #elf.device                 = 0
        #elf.function               = 0
        self.tag                    = 0
        self.last_dw_be             = 0
        
        self.payload                = 0
        self.reserve_bit1           = 0
        self.reserve_bit2           = 0
        self.reserve_bit3           = 0
        self.reserve_bit4           = 0
        self.reserve_bit5           = 0
        self.th                     = 0
        
        self.ext_register_number    = 0
        self.register_number        = 0    
    
 
class tlp_fmt(IntEnum):
    cfgrd=0b000
    cfgwr=0b010

class tlp_type(IntEnum):
    cfgwr0=0b0001
    cfgrd0=0b0010
    cfgwr1=0b0011
    cfgrd1=0b0100


pkg = pcie_pkg()





