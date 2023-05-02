import random
from pprint import pprint

from pcie_seq_tlp_item_base_pkg import *
from pcie_com_file import *

print("hello pcie_seq_config_pkg")

class pcie_seq_rc_config_pkt(pcie_pkg):
    def __init__(self):
        super().__init__()
    def cf0_pkt(self):
        self.fmt                    = random.getrandbits(3)
        self.bdf                    = random.getrandbits(16)
        self.type                   = random.getrandbits(5)
        self.first_dw_be            = 0b0011
        self.ep                     = random.getrandbits(1)
        self.block                  = random.getrandbits(1)
        self.td                     = random.getrandbits(1)
        self.tc                     = random.getrandbits(3)
        self.attr0                  = random.getrandbits(2)
        self.attr1                  = random.getrandbits(1)
        self.at                     = random.getrandbits(2)
        self.length                 = random.getrandbits(10)

        self.bus                    = random.getrandbits(8)
        self.device                 = random.getrandbits(5)
        self.function               = random.getrandbits(3)
        self.tag                    = random.getrandbits(8)
        self.last_dw_be             = random.getrandbits(4)
        
        self.addresses              = random.getrandbits(4)


        
        ##              DICTIONARY FORMATTING           ##
        #self.packet = [self.bdf, self.conf_type, self.block, self.ep, self.td]
        #pkt_dict["bdf"] = self.bdf 
        #pkt_dict["conf_type"] = self.conf_type 
        #pkt_dict["block"] = self.block 
        #pkt_dict["ep"] = self.ep 
        #pkt_dict["td"] = self.td
        #pkt_dict["fmt"] = self.fmt
        #pkt_dict["first_dw_be"] = self.first_dw_be
        ##              DICTIONARY FORMATTING           ##
       
        ##                  QUEUE  FORMATTING           ##
        pkt_queue.put(format(self.fmt,'03b'))
        pkt_queue.put(format(self.type,'05b'))
        pkt_queue.put(hex(self.bdf))
        pkt_queue.put(format(self.first_dw_be,'04b'))
        pkt_queue.put(self.ep)
        pkt_queue.put(self.td)
        pkt_queue.put(hex(self.register_number))
        pkt_queue.put(self.block)
        
        pkt_queue.put(self.fmt)         
        pkt_queue.put(self.bdf)         
        pkt_queue.put(self.type)        
        pkt_queue.put(self.first_dw_be) 
        pkt_queue.put(self.ep)          
        pkt_queue.put(self.block)       
        pkt_queue.put(self.td)          
        pkt_queue.put(self.tc)          
        pkt_queue.put(self.attr0)       
        pkt_queue.put(self.attr1)       
        pkt_queue.put(self.at)          
        pkt_queue.put(self.length)      
                       
        pkt_queue.put(self.bus)         
        pkt_queue.put(self.device)      
        pkt_queue.put(self.function)    
        pkt_queue.put(self.tag)         
        pkt_queue.put(self.last_dw_be)  
                       
        pkt_queue.put(self.addresses)   





                  

    def print_bdf(self):
        print('Generated packet: BDF = {}, config type {} for {}, {}, pkt is {}, ECRC is {}, fmt is {}, first_dw_be is {}'.format(self.bdf, self.conf_type, "Switch" if self.conf_type else "end-point", "Blocking" if self.block else "Non-blocking", "Poisoned" if self.ep else "Not poisoned", "Enabled" if self.td else "Disabled", self.fmt, self.first_dw_be))
        #print(self.packet)



p1 = pcie_seq_rc_config_pkt()
