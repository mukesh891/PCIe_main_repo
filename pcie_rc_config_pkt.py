import random
from pprint import pprint

from pcie_seq_tlp_item_base_pkg import *
from pcie_com_file import *
import queue
print("hello pcie_seq_config_pkg")
f = open("hex_file.txt","w")
class pcie_seq_rc_config_pkt(pcie_pkg):
    def __init__(self):
        super().__init__()
    def cf0_pkt(self):
        for i in range(100):
            self.pkt_queue = queue.Queue()
            self.fmt                    = random.getrandbits(3)
            ##    BDF format for requester and completer    ##
            self.requester_id           = random.getrandbits(16)
            self.completer_id           = random.getrandbits(16)
            ##################################################
            self.type                   = random.getrandbits(5)
            self.first_dw_be            = 0b0011
            self.ep                     = random.getrandbits(1) 
            self.td                     = random.getrandbits(1)
            self.tc                     = random.getrandbits(3)
            self.attr0                  = random.getrandbits(2)
            self.attr1                  = random.getrandbits(1)
            self.at                     = random.getrandbits(2)
            self.length                 = random.getrandbits(10)

            #self.bus                    = random.getrandbits(8)
            #elf.device                 = random.getrandbits(5)
            #elf.function               = random.getrandbits(3)
            self.tag                    = random.getrandbits(8)
            self.last_dw_be             = random.getrandbits(4)
            
            self.payload                = random.getrandbits(32)
            self.reserve_bit1           = random.choice([0,1])
            self.reserve_bit2           = random.choice([0,1])
            self.reserve_bit3           = random.choice([0,1])
            self.reserve_bit4           = random.choice([0,15])
            self.reserve_bit5           = random.choice([0,3])
            self.th                     = random.choice([0,1])
            
            self.ext_register_number    = random.choice([0,15])
            self.register_number        = random.choice([0,63])
 

            #fdb_str = format(self.first_dw_be, '04b')

            fmt_str                 =format(self.fmt, '03b')       
            requester_id_str        =format(self.requester_id, '016b')       
            completer_id_str        =format(self.completer_id, '016b')       
            type_str                =format(self.type, '05b')      
            first_dw_be_str=format(self.first_dw_be, '04b')
            ep_str                  =format(self.ep, '01b')        
            td_str                  =format(self.td, '01b')        
            tc_str                  =format(self.tc, '03b')        
            attr0_str               =format(self.attr0, '02b')     
            attr1_str               =format(self.attr1, '01b')     
            at_str                  =format(self.at, '02b')        
            length_str              =format(self.length, '010b')    
            #bus_str        =format(self.bus, '08b')       
            #device_str     =format(self.device, '05b')    
            #function_str   =format(self.function, '03b')  
            tag_str                 =format(self.tag, '08b')       
            last_dw_be_str          =format(self.last_dw_be, '04b') 
            reserve_bit4_str        =format(self.reserve_bit4, '04b')
            
            ext_register_number_str=format(self.ext_register_number, '04b')
            register_number_str=format(self.register_number, '06b')
                         
            #addresses  =format(self.addresses, '04b')
            reserve_bit5_str=  format(self.reserve_bit5, '02b')

            payload_str     = format(self.payload, '032b')
            #print(str(fmt_str)+
            #        str(type_str)+
            #        str(self.reserve_bit1)+
            #str(tc_str        )+
            #str(self.reserve_bit2)+
            #str(attr1_str     )+
            #str(self.reserve_bit3)+
            #str(self.th)+
            #str(td_str        )+
            #str(ep_str        )+
            #str(attr0_str     )+
            #str(at_str        )+
            #str(length_str    )+
            ##str(requester_bdf_str)+
            #str(requester_id_str)+
            #str(tag_str       )+
            #str(last_dw_be_str)+
            #str(first_dw_be_str)+
            #str(completer_id_str)+
            #str(reserve_bit4_str)+
            #str(ext_register_number_str)+
            #str(register_number_str)
            #)


            header = (str(fmt_str)+str(type_str)+str(self.reserve_bit1)+
            str(tc_str        )+str(self.reserve_bit2)+
            str(attr1_str     )+
            str(self.reserve_bit3)+
            str(self.th)+
            str(td_str        )+
            str(ep_str        )+
            str(attr0_str     )+
            str(at_str        )+
            str(length_str    )+
            #str(requester_bdf_str)+
            str(requester_id_str)+
            str(tag_str       )+
            str(last_dw_be_str)+
            str(first_dw_be_str)+
            str(completer_id_str)+
            str(reserve_bit4_str)+
            str(ext_register_number_str)+
            str(register_number_str)+
            str(reserve_bit5_str)+
            str(payload_str))
            
            pkt_queue.put(header)
            f.write(header)
            f.write("\n")

cls=pcie_seq_rc_config_pkt()
cls.cf0_pkt()              
for i in range (100):
    q = pkt_queue.get()
    print(q)

  #      def print_bdf(self):
  #          print('Generated packet: BDF = {}, config type {} for {}, {}, pkt is {}, ECRC is {}, fmt is {}, first_dw_be is {}'.format(self.bdf, self.conf_type, "Switch" if self.conf_type else "end-point", "Blocking" if self.block else "Non-blocking", "Poisoned" if self.ep else "Not poisoned", "Enabled" if self.td else "Disabled", self.fmt, self.first_dw_be))
  #         #print(self.packet)



p1 = pcie_seq_rc_config_pkt()
p1.cf0_pkt()
f.close()
