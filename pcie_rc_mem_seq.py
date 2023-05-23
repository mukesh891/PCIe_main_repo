from pcie_lib import *
from pcie_seq_tlp_item_base_pkg import *
from pcie_rc_com_file import *
from pcie_com_file import *
import queue
print("hello pcie_rc_mem_seq")
#gen_f = open("gen_logs/generator_out.txt","w")
#bin_f = open("gen_logs/bin_file.txt","a") #Openning a file in binary format
class pcie_rc_mem_seq(pcie_pkg): #Extending from base class
    def __init__(self):
        self.num_pkts=argv.num_pkts        
        self.err_eij = argv.err_eij
        self.err_pkt_no = argv.err_pkt_no
        self.tx_no = 0
        self.iter = 0
        '''
        self.arr =[0]*self.err_pkt_no
        self.arr_t =[0]*self.err_pkt_no
        for i in range(0,self.err_pkt_no):
            self.arr_t[i] = random.randrange(self.num_pkts)
            self.arr = list(set(self.arr_t))
            self.arr.sort()
        
        print(self.arr)
        print(len(self.arr))
        print(self.num_pkts)
        '''
        super().__init__()
        self.raddr = 0
        self.temp =0
    def mem_pkt(self):
        self.fmt                     = random.choice([0,2])  # 000 = MemRd without data, 010 = MemWr with data
        ##    BDF format for requester and completer    ##
        self.requester_id            = random.getrandbits(16)
        ##################################################
        self.type                   = random.choice([0])    # 0000b = Memory Read or write
        self.ep                     = 0 
        self.td                     = 0
        self.tc                     = 0 
        self.attr0                  = 0 
        self.attr1                  = 0 
        self.at                     = 0
        self.length                 = 1 
        self.tag                    = 0 
        self.addresses              = 0
        if(self.length > 1):
            self.first_dw_be            = random.getrandbits(4)
            self.last_dw_be             = random.getrandbits(4) 
        elif(self.length ==1):
            self.first_dw_be            = random.getrandbits(4)
            self.last_dw_be             = 0 
        

       ##### initializing reserved bits to zero ########
        self.reserve_bit1           = 0
        self.reserve_bit2           = 0
        self.reserve_bit3           = 0
        self.reserve_bit4           = 0
        self.reserve_bit5           = 0
        ###### Only for FMT = 010b, there will be paylod###########
        self.raddr = self.temp


        if (self.iter%2 ==0):
            #print("write",self.iter)
            self.fmt = 2
            self.type = 0
            self.payload    = random.getrandbits(32)
            self.addresses = random.getrandbits(30)
            self.addresses -= self.addresses % 4
            #print(self.addresses)
        elif (self.iter %2==1):
            #print("->read ",self.iter)
            self.type = 0
            self.fmt = 0
            self.addresses = self.raddr
            #print(self.addresses)
            self.payload    = 0
        self.temp=self.addresses


    def run_mem(self):
        self.mem_pkt()
        ## converting all the values to bin format ##
        fmt_str                 =format(self.fmt, '03b')       
        requester_id_str        =format(self.requester_id, '016b')             
        type_str                =format(self.type, '05b')      
        first_dw_be_str         =format(self.first_dw_be, '04b')
        ep_str                  =format(self.ep, '01b')        
        td_str                  =format(self.td, '01b')        
        tc_str                  =format(self.tc, '03b')        
        attr0_str               =format(self.attr0, '02b')     
        attr1_str               =format(self.attr1, '01b')     
        at_str                  =format(self.at, '02b')        
        length_str              =format(self.length, '010b')      
        tag_str                 =format(self.tag, '08b')       
        last_dw_be_str          =format(self.last_dw_be, '04b') 
        reserve_bit4_str        =format(self.reserve_bit4, '01b')               
        addresses_str           =format(self.addresses, '030b')
        reserve_bit5_str        =format(self.reserve_bit5, '01b') 
        payload_str             = format(self.payload, '032b')
        ###############################################
        
        ## Concatenating all the value into tlp_pkt in string format of binary value ##
        tlp_packet = (str(fmt_str)+str(type_str)+str(self.reserve_bit1)+
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
        str(addresses_str)+
        str(reserve_bit4_str)+
        str(reserve_bit5_str)+
        str(payload_str))
        ##################################################################################
         
        ## puting the tlp_packet into queue ##
        g_pkt_queue.put(tlp_packet)
        self.iter = self.iter+1
        #print("->",tlp_packet)
        ## Writing the tlp_packet into the hex_fil.txt ##

