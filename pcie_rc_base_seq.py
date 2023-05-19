from pcie_rc_config_pkt import *
from pcie_rc_mem_seq import *
from pcie_com_file import *
from pcie_rc_com_file import *
from pcie_rc_generated_logs import *
#bin_f = open("gen_logs/bin_file.txt","w")
#gen_f = open("gen_logs/generator_out.txt","w")
class pcie_rc_base_seq:
    def __init__(self):
        num_pkts = argv.num_pkts
        super().__init__()
        self.which_seq = 0
    def run(self):
        print("Main sequence executed")
        cfg_seq = pcie_rc_config_pkt()
        mem_seq = pcie_rc_mem_seq()
        for i in range(num_pkts): # as we are sending 128bits
            #First 10 packets has be config type
            if(i > 10):     
                self.which_seq = random.choice([0,1]) # Either Mem or cfg
                if( self.which_seq == 0):
                    cfg_seq.run_cfg()

                if( self.which_seq == 1):
                    mem_seq.run_mem()
            else:
                cfg_seq = pcie_rc_config_pkt()
                cfg_seq.run_cfg()
            #    if __name__ == "__main__":
            #        seq.run()
for i in range(g_pkt_queue.qsize()):
            bin_q = g_pkt_queue
            q = bin_q.get()
            print("the g pkt q is ->",q)

base_seq =pcie_rc_base_seq()
base_seq.run()
bin_f.close()        
gen_f.close()        
g_log=pcie_rc_generated_logs()
g_log.bin_file_handle()
g_log.hex_file_handle()





   #def bin_file_handle(self):
   #    #for i in range(100):
   #    self.cfg0_pkt()
   #    ## converting all the values to bin format ##
   #    #if(self.err_eij):
   #    #   if self.k in arr:
   #    #       print("k value is ->",self.k)
   #    #       err_dict=j
   #    #       for err_dict in err_enum_q:
   #    #           err_id=self.k 
   #    #           print("ERROR_ID =",err_id)
   #    #           if err_id in err_dict:
   #    #               #print("i value is ->",i)
   #    #               print(err_dict[err_id])
   #    #   for i in arr:
   #    #       if(i==self.k):
   #    #           self.fmt_eij_err()
   #    #           print(self.fmt)
   #    #           self.j=self.j+1
   #    #           '''
   #    #           if (arr[self.j]==self.k or self.j < len(arr)-1):
   #    #               self.fmt_eij_err()
   #    #               print(self.fmt)
   #    #               self.j=self.j+1
   #    #           ''' 
   #    self.k=self.k+1
   #    fmt_str                 =format(self.fmt, '03b')       
   #    requester_id_str        =format(self.requester_id, '016b')       
   #    completer_id_str        =format(self.completer_id, '016b')       
   #    type_str                =format(self.type, '05b')      
   #    first_dw_be_str         =format(self.first_dw_be, '04b')
   #    ep_str                  =format(self.ep, '01b')        
   #    td_str                  =format(self.td, '01b')        
   #    tc_str                  =format(self.tc, '03b')        
   #    attr0_str               =format(self.attr0, '02b')     
   #    attr1_str               =format(self.attr1, '01b')     
   #    at_str                  =format(self.at, '02b')        
   #    length_str              =format(self.length, '010b')    
   #    #bus_str        =format(self.bus, '08b')       
   #    #device_str     =format(self.device, '05b')    
   #    #function_str   =format(self.function, '03b')  
   #    tag_str                 =format(self.tag, '08b')       
   #    last_dw_be_str          =format(self.last_dw_be, '04b') 
   #    reserve_bit4_str        =format(self.reserve_bit4, '04b')
   #    
   #    ext_register_number_str =format(self.ext_register_number, '04b')
   #    register_number_str     =format(self.register_number, '06b')
   #                 
   #    #addresses  =format(self.addresses, '04b')
   #    reserve_bit5_str        =format(self.reserve_bit5, '02b')
   #    
   #    payload_str             = format(self.payload, '032b')
   #    ###############################################
   #    
   #    ## Concatenating all the value into tlp_pkt in string format of binary value ##
   #    tlp_packet = (str(fmt_str)+str(type_str)+str(self.reserve_bit1)+
   #    str(tc_str        )+str(self.reserve_bit2)+
   #    str(attr1_str     )+
   #    str(self.reserve_bit3)+
   #    str(self.th)+
   #    str(td_str        )+
   #    str(ep_str        )+
   #    str(attr0_str     )+
   #    str(at_str        )+
   #    str(length_str    )+
   #    str(requester_id_str)+
   #    str(tag_str       )+
   #    str(last_dw_be_str)+
   #    str(first_dw_be_str)+
   #    str(completer_id_str)+
   #    str(reserve_bit4_str)+
   #    str(ext_register_number_str)+
   #    str(register_number_str)+
   #    str(reserve_bit5_str)+
   #    str(payload_str))
   #    ##################################################################################
   #    
   #    ## puting the tlp_packet into queue ##
   #    g_pkt_queue.put(tlp_packet)
   #    print("->",tlp_packet)
   #    print("len of tlp pkt",len(tlp_packet))
   #    ## Writing the tlp_packet into the hex_fil.txt ##
   #    bin_f.write(tlp_packet)
   #    bin_f.write("\n")
   #    print("len of tlp pkt after n",len(tlp_packet))
   #    #bin_f.close()
   #    
   #def hex_file_handle(self):
   #    bin_f = open("gen_logs/bin_file.txt","r")
   #    hex_f = open("gen_logs/hex_file.txt","w")
   #    for line in bin_f:
   #        line = "0b" + line
   #        hex_val = hex(int(line,2))[2:]
   #        hex_val = str(hex_val)
   #        if len(hex_val)==32:
   #            hex_f.write(hex_val)
   #        else:
   #            hex_val = ("0"*(32-len(hex_val)))+hex_val
   #            hex_f.write(hex_val)
   #        print(hex_val)
   #        hex_f.write("\n")
   #    hex_f.close()
   #    bin_f.close()
   #def gen_log(self):
   #     
   #    gen_f = open("gen_logs/generator_out.log","w")
   #        
   #    num_pkts=argv.num_pkts        
   #    for i in range(num_pkts):
   #        self.cfg0_pkt()
   #        self.bin_file_handle()
   #        gen_f.write("---------------------------------- TLP ")
   #        gen_f.write(str(i))
   #        gen_f.write(" --------------------------------------- ")
   #        gen_f.write("\n")
   #        '''
   #        Memory Read Request (MRd)                   000=3DW, no data 001=4DW, no data 00000
   #                                                    
   #        Memory Read Lock Request (MRdLk)            000= 3DW, no data 001=4DW, no data 0 0001
   #                                                    
   #        Memory Write Request (MWr)                  010 3DW, w/ data 011=4DW, w/ data 00000
   #                                                    
   #        IO Read Request (IORd)                      000=3DW, no data 0 0010
   #                                                    
   #        IO Write Request (IOWr)                     010=3DW, w/ data 0 0010
   #        
   #        Config Type 0 Read Request (CfgRd0)|        000=3DW, no data 0 0100
   #        
   #        Config Type 0 Write Request (CfgWr0)        010=3DW, w/ data 00100
   #        
   #        Config Type 1 Read Request (CfgRd1)         000=3DW, no data 0 0101
   #        
   #        Config Type 1 Write Request (CfgWr1)        010=3DW, w/ data 00101
   #        
   #        Message Request (Msg)                       001=4DW, no data 10 rrr* (see routing field)
   #        
   #        Message Request W/Data (MsgD)               011=4DW, w/ data 1 Orrr* (see routing field)
   #        
   #        
   #        Completion (Cpl)                            000=3DW, no data 0 1010
   #        
   #        Completion W/Data (CpID)                    010=3DW, w/data  0 1010
   #        
   #        Completion-Locked (CpILk)                   000=3DW, no data 0 1011
   #        
   #        Completion W/Data (CplDLk)                  010=3DW, w/ data 0 1011
   #        
   #        Fetch and Add AtomicOp Request              010=3DW, w/ data 011-4DW, w/ data 0 1100
   #        '''

   #        if((self.fmt==0) and (self.type==0)): 
   #             gen_f.write("Memory Read Request (MRd) with 3DW, no data           ")
   #             gen_f.write("\n")
   #        if((self.fmt==1) and (self.type==0)): 
   #             gen_f.write("Memory Read Request (MRd) with 4DW, no data           ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==0) and (self.type==1)): 
   #             gen_f.write("Memory Read Lock Request (MRdLk) with 3DW, no data     ")
   #             gen_f.write("\n")
   #        if((self.fmt==1) and (self.type==1)): 
   #             gen_f.write("Memory Read Lock Request (MRdLk) with 4DW, no data     ")
   #             gen_f.write("\n")
   #                          
   #        if((self.fmt==2) and (self.type==0)):
   #             gen_f.write("Memory Write Request (MWr) with 3DW, with data         ")
   #             gen_f.write("\n")
   #        if((self.fmt==3) and (self.type==0)):                         
   #             gen_f.write("Memory Write Request (MWr) with 4DW, with data         ")
   #             gen_f.write("\n")
   #            
   #        if((self.fmt==0) and (self.type==2)): 
   #             gen_f.write("IO Read Request (IORd) with 3DW, no data               ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==2)): 
   #             gen_f.write("IO Write Request (IOWr) with 3DW, with data    ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==0) and (self.type==4)): 
   #             gen_f.write("Config Type 0 Read Request (CfgRd0) with 3DW, no data")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==4)): 
   #             gen_f.write("Config Type 0 Write Request (CfgWr0) with 3DW, with data")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==0) and (self.type==5)): 
   #             gen_f.write("Config Type 1 Read Request (CfgRd1) with 3DW, no data")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==5)): 
   #             gen_f.write("Config Type 1 Write Request (CfgWr1) with 3DW, with data")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==1) and (self.type==16)): 
   #             gen_f.write("Message Request (Msg) with 4DW, no data              ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==3) and (self.type==16)): 
   #             gen_f.write("Message Request W/Data (MsgD) with 4DW, with data      ")
   #             gen_f.write("\n")
   #             
   #             
   #        if((self.fmt==0) and (self.type==10)): 
   #             gen_f.write("Completion (Cpl) with 3DW, no data                   ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==10)): 
   #             gen_f.write("Completion W/Data (CpID) with 3DW, with data           ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==0) and (self.type==11)): 
   #             gen_f.write("Completion-Locked (CpILk) with 3DW, no data          ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==11)): 
   #             gen_f.write("Completion W/Data (CplDLk) with 3DW, with data         ")
   #             gen_f.write("\n")
   #             
   #        if((self.fmt==2) and (self.type==12)): 
   #             gen_f.write("Fetch and Add AtomicOp Request with 3DW, with data     ")
   #             gen_f.write("\n")
   #        if((self.fmt==3) and (self.type==12)): 
   #             gen_f.write("Fetch and Add AtomicOp Request with 3DW, with data     ")
   #             gen_f.write("\n")


   #        gen_f.write("fmt = ")
   #        gen_f.write(hex(self.fmt))
   #        gen_f.write("\n")
   #        gen_f.write("type = ")
   #        gen_f.write(hex(self.type))
   #        gen_f.write("\n")
   #        gen_f.write("reserve_bit1 = ")
   #        gen_f.write(hex(self.reserve_bit1))       
   #        gen_f.write("\n")
   #        gen_f.write("tc = ")
   #        gen_f.write(hex(self.tc       ))
   #        gen_f.write("\n")
   #        gen_f.write("reserve_bit2 = ")
   #        gen_f.write(hex(self.reserve_bit2))       
   #        gen_f.write("\n")
   #        gen_f.write("attr1 = ")
   #        gen_f.write(hex(self.attr1       ))
   #        gen_f.write("\n")
   #        gen_f.write("reserve_bit3 = ")
   #        gen_f.write(hex(self.reserve_bit3))       
   #        gen_f.write("\n")
   #        gen_f.write("th = ")  
   #        gen_f.write(hex(self.th          ))  
   #        gen_f.write("\n")
   #        gen_f.write("td = ")  
   #        gen_f.write(hex(self.td          ))  
   #        gen_f.write("\n")
   #        gen_f.write("ep = ") 
   #        gen_f.write(hex(self.ep          )) 
   #        gen_f.write("\n")
   #        gen_f.write("attr0 = ")
   #        gen_f.write(hex(self.attr0       ))
   #        gen_f.write("\n")
   #        gen_f.write("at = ")
   #        gen_f.write(hex(self.at          ))
   #        gen_f.write("\n")
   #        gen_f.write("length = ")
   #        gen_f.write(hex(self.length      ))
   #        gen_f.write("\n")
   #        gen_f.write("requester_id = ")
   #        gen_f.write(hex(self.requester_id))
   #        gen_f.write("\n")
   #        gen_f.write("tag = ")
   #        gen_f.write("\n")


   #        gen_f.write(hex(self.tag         ))
   #        gen_f.write("\n")
   #        gen_f.write("last_dw_be = ")
   #        gen_f.write(hex(self.last_dw_be  ))
   #        gen_f.write("\n")
   #        gen_f.write("first_dw_be = ")
   #        gen_f.write(hex(self.first_dw_be ))
   #        gen_f.write("\n")
   #        gen_f.write("completer_id = ")
   #        gen_f.write(hex(self.completer_id))
   #        gen_f.write("\n")
   #        gen_f.write("reserve_bit4 = ")
   #        gen_f.write(hex(self.reserve_bit4))
   #        gen_f.write("\n")
   #        gen_f.write("ext_register_number = ")
   #        gen_f.write(hex(self.ext_register_number))
   #        gen_f.write("\n")
   #        gen_f.write("register_number = ")
   #        gen_f.write(hex(self.register_number))    
   #        gen_f.write("\n")
   #        gen_f.write("reserve_bit5 = ")
   #        gen_f.write(hex(self.reserve_bit5))       
   #        gen_f.write("\n")
   #        gen_f.write("payload = ")
   #        gen_f.write(hex(self.payload)      )      
   #        gen_f.write("\n")
   #        gen_f.write("\n")
   #    bin_f.close()        
   #    self.hex_file_handle()

