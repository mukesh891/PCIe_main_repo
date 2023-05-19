from pcie_lib import *
from pcie_seq_tlp_item_base_pkg import *
from pcie_rc_com_file import *
from pcie_com_file import *
import queue
print("hello pcie_rc_mem_seq")
gen_f = open("gen_logs/generator_out.txt","w")
bin_f = open("gen_logs/bin_file.txt","a") #Openning a file in binary format
class pcie_rc_mem_seq(pcie_pkg): #Extending from base class
    def __init__(self):
        self.num_pkts=argv.num_pkts        
        self.err_eij = argv.err_eij
        self.err_pkt_no = argv.err_pkt_no
        self.tx_no = 0
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
    def mem_pkt(self):
            self.fmt                     = random.choice([0,2])  # 000 = MemRd without data, 010 = MemWr with data
        ##    BDF format for requester and completer    ##
            self.requester_id            = random.getrandbits(16)
        ##################################################
            self.type                   = random.choice([0])    # 0000b = Memory Read or write
            self.ep                     = 0 
            self.td                     = 0
            self.tc                     = random.getrandbits(3) # 000b - 111b ( Higher TC value will be higher priority )
            self.attr0                  = random.choice([0,2])  # 2bit, we need 00 and 10
            self.attr1                  = random.getrandbits(1) # 1bit
            self.at                     = 0
            self.length                 = random.choice([1]) 
            self.tag                    = random.getrandbits(8)
            if(self.length > 1):
              self.first_dw_be            = random.getrandbits(4)
              self.last_dw_be             = random.getrandbits(4) 
            elif(self.length ==1):
                 self.first_dw_be            = random.getrandbits(4)
                 self.last_dw_be             = 0 
        
       ########## Only for FMT = 010b, there will be paylod###########
            if (self.fmt==2):
               self.payload                = random.getrandbits(32)
            else:
               self.payload                = 0
       ######### initializing reserved bits to zero ########
            self.reserve_bit1           = 0
            self.reserve_bit2           = 0
            self.reserve_bit3           = 0
            self.reserve_bit4           = 0
            self.reserve_bit5           = 0
            self.addresses                =  random.getrandbits(30)

    #def bin_file_handle(self):
    def run_mem(self):
        #for i in range(100):
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
        print("->",tlp_packet)
        ## Writing the tlp_packet into the hex_fil.txt ##
'''  
    def hex_file_handle(self):
        bin_f = open("bin_file.txt","r")
        hex_f = open("hex_file.txt","w")
        for line in bin_f:
            line = "0b" + line
            hex_val = hex(int(line,2))[2:]
            hex_val = str(hex_val)
            if len(hex_val)==32:
                hex_f.write(hex_val)
            else:
                hex_val = ("0"*(32-len(hex_val)))+hex_val
                hex_f.write(hex_val)
            print(hex_val)
            hex_f.write("\n")
        hex_f.close()
        bin_f.close()
    def gen_log(self):
         
        #gen_f = open("genearator_out.log","w")
            
        #num_pkts=argv.num_pkts        
        #for i in range(num_pkts):
        self.mem_pkt()
        self.bin_file_handle()
        gen_f.write("---------------------------------- TLP ")
        gen_f.write(str(self.tx_no))
        gen_f.write(" --------------------------------------- ")
        gen_f.write("\n")
        
        Memory Read Request (MRd)                   000=3DW, no data 001=4DW, no data 00000
                                                    
        Memory Read Lock Request (MRdLk)            000= 3DW, no data 001=4DW, no data 0 0001
                                                    
        Memory Write Request (MWr)                  010 3DW, w/ data 011=4DW, w/ data 00000
                                                    
        IO Read Request (IORd)                      000=3DW, no data 0 0010
                                                    
        IO Write Request (IOWr)                     010=3DW, w/ data 0 0010
        
        Config Type 0 Read Request (CfgRd0)|        000=3DW, no data 0 0100
        
        Config Type 0 Write Request (CfgWr0)        010=3DW, w/ data 00100
        
        Config Type 1 Read Request (CfgRd1)         000=3DW, no data 0 0101
        
        Config Type 1 Write Request (CfgWr1)        010=3DW, w/ data 00101
        
        Message Request (Msg)                       001=4DW, no data 10 rrr* (see routing field)
        
        Message Request W/Data (MsgD)               011=4DW, w/ data 1 Orrr* (see routing field)
        
        
        Completion (Cpl)                            000=3DW, no data 0 1010
        
        Completion W/Data (CpID)                    010=3DW, w/data  0 1010
        
        Completion-Locked (CpILk)                   000=3DW, no data 0 1011
        
        Completion W/Data (CplDLk)                  010=3DW, w/ data 0 1011
        
        Fetch and Add AtomicOp Request              010=3DW, w/ data 011-4DW, w/ data 0 1100
        

        if((self.fmt==0) and (self.type==0)): 
             gen_f.write("Memory Read Request (MRd) with 3DW, no data           ")
             gen_f.write("\n")
                          
        if((self.fmt==2) and (self.type==0)):
             gen_f.write("Memory Write Request (MWr) with 3DW, with data         ")
             gen_f.write("\n")                 
             
        if((self.fmt==0) and (self.type==10)): 
             gen_f.write("Completion (Cpl) with 3DW, no data                   ")
             gen_f.write("\n")
             
        if((self.fmt==2) and (self.type==10)): 
             gen_f.write("Completion W/Data (CpID) with 3DW, with data           ")
             gen_f.write("\n")

        gen_f.write("fmt = ")
        gen_f.write(hex(self.fmt))
        gen_f.write("\n")
        gen_f.write("type = ")
        gen_f.write(hex(self.type))
        gen_f.write("\n")
        gen_f.write("reserve_bit1 = ")
        gen_f.write(hex(self.reserve_bit1))       
        gen_f.write("\n")
        gen_f.write("tc = ")
        gen_f.write(hex(self.tc       ))
        gen_f.write("\n")
        gen_f.write("reserve_bit2 = ")
        gen_f.write(hex(self.reserve_bit2))       
        gen_f.write("\n")
        gen_f.write("attr1 = ")
        gen_f.write(hex(self.attr1       ))
        gen_f.write("\n")
        gen_f.write("reserve_bit3 = ")
        gen_f.write(hex(self.reserve_bit3))       
        gen_f.write("\n")
        gen_f.write("th = ")  
        gen_f.write(hex(self.th          ))  
        gen_f.write("\n")
        gen_f.write("td = ")  
        gen_f.write(hex(self.td          ))  
        gen_f.write("\n")
        gen_f.write("ep = ") 
        gen_f.write(hex(self.ep          )) 
        gen_f.write("\n")
        gen_f.write("attr0 = ")
        gen_f.write(hex(self.attr0       ))
        gen_f.write("\n")
        gen_f.write("at = ")
        gen_f.write(hex(self.at          ))
        gen_f.write("\n")
        gen_f.write("length = ")
        gen_f.write(hex(self.length      ))
        gen_f.write("\n")
        gen_f.write("requester_id = ")
        gen_f.write(hex(self.requester_id))
        gen_f.write("\n")
        gen_f.write("tag = ")
        gen_f.write("\n")


        gen_f.write(hex(self.tag         ))
        gen_f.write("\n")
        gen_f.write("last_dw_be = ")
        gen_f.write(hex(self.last_dw_be  ))
        gen_f.write("\n")
        gen_f.write("first_dw_be = ")
        gen_f.write(hex(self.first_dw_be ))
        gen_f.write("\n")
        gen_f.write("addresses = ")
        gen_f.write(hex(self.addresses))
        gen_f.write("\n")
        gen_f.write("reserve_bit4 = ")
        gen_f.write(hex(self.reserve_bit4))
        gen_f.write("\n")
        gen_f.write("payload = ")
        gen_f.write(hex(self.payload)      )      
        gen_f.write("\n")
        gen_f.write("\n")
        self.tx_no=self.tx_no+1

        #bin_f.close()        
        #self.hex_file_handle()
'''
'''
    def gen_log(self):
        gen_f = open("genearator.csv","w")
        gen_f.write("fmt,")
        gen_f.write("type,")
        gen_f.write("reserve_bit1       ,")
        gen_f.write("tc       ,")
        gen_f.write("reserve_bit2       ,")
        gen_f.write("attr1       ,")
        gen_f.write("reserve_bit3       ,")
        gen_f.write("th          ,")  
        gen_f.write("td          ,")  
        gen_f.write("ep          ,") 
        gen_f.write("attr0       ,")
        gen_f.write("at          ,")
        gen_f.write("length      ,")
        gen_f.write("requester_id,")
        gen_f.write("tag         ,")
        gen_f.write("last_dw_be  ,")
        gen_f.write("first_dw_be ,")
        gen_f.write("completer_id,")
        gen_f.write("reserve_bit4,")
        gen_f.write("ext_register_number,")
        gen_f.write("register_number    ,")
        gen_f.write("reserve_bit5       ,")
        gen_f.write("payload            ,")
        gen_f.write("\n")


        num_pkts=argv.num_pkts        
        for i in range(num_pkts):
            self.cfg0_pkt()
            self.bin_file_handle()
            
               
            gen_f.write(hex(self.fmt))
            gen_f.write(",")
            gen_f.write(hex(self.type))
            gen_f.write(",")
            gen_f.write(hex(self.reserve_bit1))       
            gen_f.write(",")
            gen_f.write(hex(self.tc       ))
            gen_f.write(",")
            gen_f.write(hex(self.reserve_bit2))       
            gen_f.write(",")
            gen_f.write(hex(self.attr1       ))
            gen_f.write(",")
            gen_f.write(hex(self.reserve_bit3))       
            gen_f.write(",")
            gen_f.write(hex(self.th          ))  
            gen_f.write(",")
            gen_f.write(hex(self.td          ))  
            gen_f.write(",")
            gen_f.write(hex(self.ep          )) 
            gen_f.write(",")
            gen_f.write(hex(self.attr0       ))
            gen_f.write(",")
            gen_f.write(hex(self.at          ))
            gen_f.write(",")
            gen_f.write(hex(self.length      ))
            gen_f.write(",")
            gen_f.write(hex(self.requester_id))
            gen_f.write(",")
            gen_f.write(hex(self.tag         ))
            gen_f.write(",")
            gen_f.write(hex(self.last_dw_be  ))
            gen_f.write(",")
            gen_f.write(hex(self.first_dw_be ))
            gen_f.write(",")
            gen_f.write(hex(self.completer_id))
            gen_f.write(",")
            gen_f.write(hex(self.reserve_bit4))
            gen_f.write(",")
            gen_f.write(hex(self.ext_register_number))
            gen_f.write(",")
            gen_f.write(hex(self.register_number))    
            gen_f.write(",")
            gen_f.write(hex(self.reserve_bit5))       
            gen_f.write(",")
            gen_f.write(hex(self.payload)      )      
            gen_f.write("\n")
        bin_f.close()
        self.hex_file_handle()
'''
#c = pcie_rc_mem_seq()
#c.bin_file_handle()
#c.file_handle()
#c.hex_file_handle()
#c.mix_pkt()
#c.gen_log()
