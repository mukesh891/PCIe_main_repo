import random
from pprint import pprint

from pcie_seq_tlp_item_base_pkg import *
from pcie_com_file import *

print("hello pcie_seq_config_pkg")

class pcie_seq_rc_config_pkt(pcie_pkg):
    def __init__(self):
        super().__init__()
    def cf0_pkt(self):
        self.fmt = random.getrandbits(3)
        self.bdf = random.getrandbits(17)
        self.cfg_type = random.getrandbits(1)
        self.first_dw_be = 0b0011
        self.ep = random.getrandbits(1)
        self.block = random.getrandbits(1)
        self.td= random.getrandbits(1)

        
        #self.packet = [self.bdf, self.conf_type, self.block, self.ep, self.td]
        pkt_dict["bdf"] = self.bdf 
        pkt_dict["conf_type"] = self.conf_type 
        pkt_dict["block"] = self.block 
        pkt_dict["ep"] = self.ep 
        pkt_dict["td"] = self.td
        pkt_dict["fmt"] = self.fmt
        pkt_dict["first_dw_be"] = self.first_dw_be
       

                  

    def print_bdf(self):
        print('Generated packet: BDF = {}, config type {} for {}, {}, pkt is {}, ECRC is {}, fmt is {}, first_dw_be is {}'.format(self.bdf, self.conf_type, "Switch" if self.conf_type else "end-point", "Blocking" if self.block else "Non-blocking", "Poisoned" if self.ep else "Not poisoned", "Enabled" if self.td else "Disabled", self.fmt, self.first_dw_be))
        #print(self.packet)



p1 = pcie_seq_rc_config_pkt()
