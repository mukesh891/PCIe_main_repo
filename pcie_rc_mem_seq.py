from pcie_lib import *
from pcie_seq_tlp_item_base_pkg import *
from pcie_rc_com_file import *
from pcie_com_file import *
import queue
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_mem_seq.py file")

class pcie_rc_mem_seq(pcie_pkg): #Extending from base class
    def __init__(self):
        self.iter = 0
        super().__init__()
        self.raddr = 0
        self.temp =0
        self.temp_1 = 0
        self.chunk_data = []
        self.i=0
        self.num_tx=0
        self.payload_str = ''
        self.prev_first_dw_be   = 0
        self.temp_addr          = 0
        self.temp_length        = 0
        self.prev_tag           = 0

        self.prev_ep            = 0
        self.prev_td            = 0
        self.prev_tc            = 0
        self.prev_attr0         = 0
        self.prev_attr1         = 0
        self.prev_at            = 0
        self.temp_num_tx        = 0
        if(DW % mps == 0):
            self.num_tx     = DW//mps 
            pass
        else:
            self.num_tx     = DW // mps + 1

        if(mps==1024):
            self.length = 0                
        else:
            self.length = DW

    def mem_pkt(self):
        self.fmt                     = random.choice([0,2])  # 000 = MemRd without data, 010 = MemWr with data
        ##    BDF format for requester and completer    ##
        #self.requester_id            = random.getrandbits(16)
        ##################################################
        self.type                   = random.choice([0])    # 0000b = Memory Read or write
        self.ep                     = 0 
        self.td                     = 1
        self.tc                     = 0 
        self.attr0                  = 0 
        self.attr1                  = 0 
        self.at                     = 0
        self.tag                    = 0 
        
       ##### initializing reserved bits to zero ########
        self.reserve_bit1           = 0
        self.reserve_bit2           = 0
        self.reserve_bit3           = 0
        self.reserve_bit4           = 0
        self.reserve_bit5           = 0

        ## Note: max payload = 1024
        
        if(self.length > 1):
            self.first_dw_be            = random.choice([10,5,9,11,13])
            self.last_dw_be             = random.randrange(1,15) 
        elif(self.length ==1):
            self.first_dw_be            = random.choice([10,5,9,11,13])
            self.last_dw_be             = 0
        elif(self.length > mps):
            logger.fatal("Length cannot be greater than 1024 i.e MAX_PAYLOAD_SIZE : 1024")
        temp_dw = DW
        mps_width = f'0{32*mps}b'
        #for j in range(6):
        if(len(self.chunk_data) == 0):
            data_payload_size   = f'0{32*DW}b'
            remaining_dw        = DW%mps
            self.data_payload   = random.getrandbits(32*DW)
            self.payload_str         =  format(self.data_payload, data_payload_size)
            num_split = len(self.payload_str)//(32*mps)
            
            ## randomizing the address for 1 tx and will be executed once in every write tx
            self.addresses      = random.randint(0,63)
            self.requester_id            = random.getrandbits(16)
            self.tag                     = random.getrandbits(8)
            
            self.addresses -= self.addresses % 4  #The purpose of this code is to ensure that self.addresses is a multiple of 4 or 4 byte aligned
            self.temp_length = self.length
            self.temp_addr       = self.addresses
            for j in range(num_split):
                self.chunk_data.append(self.payload_str[(j*mps*32) :(j+1)*mps*32])
            if remaining_dw:
                self.chunk_data.append(self.payload_str[len(self.payload_str)-(remaining_dw*32):])
        
        
        
        ## Note: Check for memory write
        if(self.iter % 2 ==0 ):
            if self.i < self.num_tx:
                self.fmt = 2
                self.type = 0
                self.prev_first_dw_be        =self.first_dw_be # Purpose of this logic is to ensure that for Mem read req first DW = write req FristDW
                prev_requester_id            =self.requester_id
                ## TODO : Implement the asme code in base file pcie_pkg
                 
                self.payload            = self.chunk_data[self.i]
                if(self.i==0):
                    pass
                else:
                    self.length              =self.length - mps
                    self.addresses           = self.addresses + mps  #The purpose of this code is to ensure that self.addresses is a multiple of 4 or 4 byte aligned
                    
                
                #if(self.i==0):
                #    self.temp_length = self.length
                #    self.temp_addr   = self.addresses
                self.i += 1
        ## Note: else do for memory read
        elif (self.iter %2==1):
            #print("->read ",self.iter)
            #if self.i < self.num_tx:
            data_payload_size   = f'0{32}b'
            self.type = 0
            self.fmt = 0
            self.first_dw_be         =self.prev_first_dw_be
            self.addresses           =self.temp_addr
            self.length              =self.temp_length
            self.tag                 =self.prev_tag
            self.ep                  =self.prev_ep            
            self.tc                  =self.prev_tc         
            self.attr0               =self.prev_attr0      
            self.attr1               =self.prev_attr1      
            self.at                  =self.prev_at         
            #print(self.addresses)
            self.data_payload   = 0
            self.payload    = format(0, data_payload_size)
            #self.payload_str             = format(self.payload, data_payload_size)
            
            self.iter = self.iter+1
            self.chunk_data.clear()
 
            
        
        
        prev_tag        =self.tag
        prev_ep         =self.ep       
        prev_td         =self.td   
        prev_tc         =self.tc   
        prev_attr0      =self.attr0
        prev_attr1      =self.attr1
        prev_at         =self.at   
        
        if(self.i==self.num_tx):
            self.i = 0
            self.iter = self.iter+1


    def run_mem_str(self):
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
        #payload_size = f'0{32*mps}b'
        #if(mps):
        #    payload_str             = format(self.payload, payload_size)
        #else:
        #    payload_str             = format(self.payload, payload_size )
        ###############################################
        
        ## Concatenating all the value into tlp_pkt in string format of binary value ##
        tlp_packet_without_ecrc = (str(fmt_str)+str(type_str)+str(self.reserve_bit1)+
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
        str(self.payload))
        ##################################################################################
         
        #ECRC Value Conversion
        integer_tlp_value = int(tlp_packet_without_ecrc,2)
        ecrc_divisor = int(fixed_ecrc_divisor, 2)
        integer_ecrc_value = integer_tlp_value % ecrc_divisor 
        #remainder = integer_value % fixed_integer_value
        ecrc_value = bin(integer_ecrc_value)[2:].zfill(32)

        if self.td:
            tlp_packet = (str(tlp_packet_without_ecrc)+str(ecrc_value))
        else:
            tlp_packet = tlp_packet_without_ecrc

        ##################################################################################

        ##putting the tlp packet into txt file ##
        #TLP_Packet_f.write(f" integer_tlp_value:{integer_tlp_value }\n ecrc_divisor :{ecrc_divisor}\n ecrc:{integer_ecrc_value}\n{tlp_packet_with_ecrc}\n") 
        #TLP_Packet_f.write(f"{tlp_packet_with_ecrc}\n")
        ## puting the tlp_packet into queue ##
        g_pkt_queue.put(tlp_packet)
        #self.iter = self.iter+1
        ## Writing the tlp_packet into the hex_fil.txt ###c = pcie_rc_mem_seq()
    def run_mem(self):

        if(self.iter % 2 ==0 ):
            for i in range(self.num_tx):
                self.mem_pkt()
                self.run_mem_str()
        else:
            self.mem_pkt()
            self.run_mem_str()



