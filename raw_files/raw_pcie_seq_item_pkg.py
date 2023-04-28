#print(pkg.__dir__())
#pprint(pkg.inspect.get_members())
#class cfg_type(IntEnum):
#   type0 =0
#   type1 =1
import vsc 
import random 
from pprint import pprint
from pcie_seq_config_pkg import *
from pcie_header_config import *

h_cfg=pcie_header_config()

class pcie_pkg:
    #string name;
    #int header;
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        self.name = name
        self.size_in_bytes = vsc.uint32_t(i=size_in_bytes)
        self.xwr = xwr
        self.header = 0
        self.tlp = 0
        self.tlp_digest = 0
        
    def tlp_data(self):
        self.header = random.getrandbits(96)
        self.tlp  = random.getrandbits(256)
        self.tlp_digest = random.getrandbits(32)
    
        h_cfg.header_fields().a=100
        q.append(vars(self))

    def print_var(self):
        pprint(vars(self))
        pprint(q)
        #pprint(vars(tlp_data()))

#class handle
pkg = pcie_pkg()
#calling tlp_data func
pkg.tlp_data()
#calling print_var func
pkg.print_var()
#cfg = pcie_header_config()

print(h_cfg.header_fields())

#class header_config:
#    def config
