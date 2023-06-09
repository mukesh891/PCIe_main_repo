from pcie_lib import *
from pcie_seq_tlp_item_base_pkg import *
from pcie_com_file import *
from err_id_creation import *
#from pcie_com_file import seq_tx_no
import queue
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_config_pkt.py file")
class pcie_rc_config_pkt(pcie_pkg):
    def __init__(self):
        self.num_pkts=argv.num_pkts        
        self.err_eij = argv.err_eij
        self.err_pkt_no = argv.err_pkt_no
        self.k=0
        self.j=0
        self.tx_no = 0
        super().__init__()
    def cfg0_pkt(self):
        self.fmt                    = random.choice([0,2])
        ##    BDF format for requester and completer    ##
        self.requester_id           = random.getrandbits(16)
        self.completer_id           = random.getrandbits(16)
        self.completer_id           = 0 
        ##################################################
        self.type                   = random.choice([4])
        self.first_dw_be            = 0b0011
        self.ep                     = 0 
        self.td                     = 0
        self.tc                     = random.getrandbits(3)
        self.tc                     = 0 
        self.attr0                  = random.getrandbits(2)
        self.attr1                  = random.getrandbits(1)
        self.attr0                  = 0 
        self.attr1                  = 0
        self.at                     = random.getrandbits(2)
        self.at                     = 0
        self.length                 = random.getrandbits(10)
        self.length                 = 1 

        #self.bus                    = random.getrandbits(8)
        #elf.device                 = random.getrandbits(5)
        #elf.function               = random.getrandbits(3)
        self.tag                    = random.getrandbits(8)
        self.last_dw_be             = random.getrandbits(4)
        self.last_dw_be             = 0 
        
        if((self.fmt==2) or (self.fmt ==3)):
            self.payload                = random.getrandbits(32)
        else:
            self.payload                = 0
        self.reserve_bit1           = random.choice([0,1])
        self.reserve_bit2           = random.choice([0,1])
        self.reserve_bit3           = random.choice([0,1])
        self.reserve_bit4           = random.choice([0,15])
        self.reserve_bit5           = random.choice([0,3])
        self.th                     = 0 
        ######### initializing reserved bits to zero ########
        self.reserve_bit1           = 0
        self.reserve_bit2           = 0
        self.reserve_bit3           = 0
        self.reserve_bit4           = 0
        self.reserve_bit5           = 0
        #####################################################

        self.ext_register_number    = random.choice([0,15])
        self.ext_register_number    = 0
        ## TODO : register last 2 bit will be zero
        self.register_number        = random.choice([0,63])
        self.register_number        =  self.register_number and 0b111100 


    #def bin_file_handle(self):
    def run_cfg(self):
        #for i in range(100):
        self.cfg0_pkt()
        self.k=self.k+1
        fmt_str                 =format(self.fmt, '03b')       
        requester_id_str        =format(self.requester_id, '016b')       
        completer_id_str        =format(self.completer_id, '016b')       
        type_str                =format(self.type, '05b')      
        first_dw_be_str         =format(self.first_dw_be, '04b')
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
        
        ext_register_number_str =format(self.ext_register_number, '04b')
        register_number_str     =format(self.register_number, '06b')
                     
        #addresses  =format(self.addresses, '04b')
        reserve_bit5_str        =format(self.reserve_bit5, '02b')
        
        payload_str             = format(self.payload, '032b')
        ###############################################
        
        ## Concatenating all the value into tlp_pkt in string format of binary value ##
        tlp_packet_without_ecrc  = (str(fmt_str)+str(type_str)+str(self.reserve_bit1)+
        str(tc_str        )+str(self.reserve_bit2)+
        str(attr1_str     )+
        str(self.reserve_bit3)+
        str(self.th)+
        str(td_str        )+
        str(ep_str        )+
        str(attr0_str     )+
        str(at_str        )+
        str(length_str    )+
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
        ##################################################################################
        
        #ECRC Value Conversion
        integer_tlp_value = int(tlp_packet_without_ecrc , 2)
        ecrc_divisor = int(fixed_ecrc_divisor, 2)
        integer_ecrc_value = integer_tlp_value % ecrc_divisor 
        #remainder = integer_value % fixed_integer_value
        ecrc_value = bin(integer_ecrc_value)[2:].zfill(32)
        tlp_packet = (str(tlp_packet_without_ecrc )+str(ecrc_value))
        ##################################################################################

        ##putting the tlp packet into txt file ##
        #TLP_Packet_f.write(f" integer_tlp_value:{integer_tlp_value }\n ecrc_divisor :{ecrc_divisor}\n ecrc:{integer_ecrc_value}\n{tlp_packet_with_ecrc}\n") 
        #TLP_Packet_f.write(f"{tlp_packet_with_ecrc}\n")
        ## puting the tlp_packet into queue ##
        g_pkt_queue.put(tlp_packet)
        #self.iter = self.iter+1
        #print("->",tlp_packet)
        ## Writing the tlp_packet into the hex_fil.txt ##
