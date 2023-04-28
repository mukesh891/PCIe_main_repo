'''import vsc
import random 
import inspect
from pprint import pprint
@vsc.randobj

class pcie_pkg:
    #self.cfg_request_seq.transaction_type == svt_pcie_driver_app_transaction::CFG_WR
    def __init__(self, name = "", size_in_bytes=0, xwr=0):
        self.transaction_type = vsc.rand_bit_t(8)
        self.bdf= vsc.rand_bit_t(16)
        self.bdf= 0x1031
        self.cfg_type = vsc.rand_bit_t(1)
        self.first_dw_be = 0b0011
        self.ep = vsc.rand_bit_t(1)
        self.block = vsc.rand_bit_t(1)
        self.payload = vsc.rand_bit_t(32)
        self.command_num = vsc.rand_uint32_t()
        self.name = name
        self.size_in_bytes = vsc.uint32_t(i=size_in_bytes)
        self.xwr = vsc.uint8_t(i=xwr)
        #self.print_var(self)
  #def print_var(self):
        print(self.transaction_type)
        print(self.bdf)
        print(self.cfg_type)
        print(self.first_dw_be)
        print(self.ep)
        print(self.block)
        print(self.payload)
        print(self.command_num)


pkg = pcie_pkg()
'''

#print(pkg.__dir__())
#pprint(pkg.inspect.get_members())
#class cfg_type(IntEnum):
#   type0 =0
#   type1 =1
import vsc 
import random 
from pprint import pprint

class pcie_pkg:
    def __init__(self, name="", size_in_bytes=0, xwr=0):
        self.transaction_type = random.getrandbits(8)
        self.bdf = random.getrandbits(16)
        self.cfg_type = random.getrandbits(1)
        self.first_dw_be = 0b0011
        self.ep = random.getrandbits(1)
        self.block = random.getrandbits(1)
        self.payload = random.getrandbits(32)
        #self.payload = vsc.rand_bit_t(32)
        self.command_num = random.getrandbits(32)
        self.name = name
        self.size_in_bytes = size_in_bytes
        self.xwr = xwr

    def print_var(self):
        pprint(vars(self))


pkg = pcie_pkg()
pkg.print_var()




