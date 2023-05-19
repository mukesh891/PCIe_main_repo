from pcie_rc_com_file import *
print("Hello this is pcie_rc_com_file")
class pcie_rc_generated_logs:
    def bin_file_handle(self):
        mixed_bin_f = open("gen_logs/bin_file.txt","w")
        for i in range(g_pkt_queue.qsize()):
            bin_q = g_pkt_queue
            q = bin_q.get()
            mixed_bin_f.write(str(q))
            mixed_bin_f.write("\n")
            print(q[:3])
        mixed_bin_f.close()
    def hex_file_handle(self):
        mixed_bin_f = open("gen_logs/bin_file.txt","r")
        hex_f = open("gen_logs/hex_file.txt","w")
        for line in mixed_bin_f:
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
        mixed_bin_f.close()

#bin_file_handle()
#hex_file_handle()

'''
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
        '''
'''
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
      
    bin_f.close()        
    self.hex_file_handle()
'''
