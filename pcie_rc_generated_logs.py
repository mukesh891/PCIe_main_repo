from pcie_rc_com_file import *
print("Hello this is pcie_rc_com_file")
class pcie_rc_generated_logs:
    def __init__(self):
        self.tx_no = 0
    def bin_file_handle(self):
        f = open("gen_logs/rc_tx_good_bin_file.txt","w")
        for i in range(g_pkt_queue.qsize()):
            bin_q = g_pkt_queue
            q = bin_q.get()
            f.write(str(q))
            f.write("\n")
            print("rc_gen_q->",q)
        f.close()
    def hex_file_handle(self):
        bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r")
        hex_f = open("gen_logs/rc_tx_good_hex_file.txt","w")
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
        bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r")
        gen_f = open("gen_logs/rc_tx_generator_out.txt","w")
        for line in bin_f:
            gen_f.write("---------------------------------- TLP ")
            gen_f.write(str(self.tx_no))
            gen_f.write(" --------------------------------------- ")
            gen_f.write("\n")
            fmt = line[0:3]		
            typ = line[3:8]
            reserve_bit1 = line[8]
            tc = line[9:12]
            reserve_bit2 = line[12]
            attr1 = line[13]
            reserve_bit3 = line[14]
            th = line[15]
            td = line[16]
            ep = line[17]
            attr0 = line[18:20]
            at = line[20:22]
            length = line[22:32]
            requester_id = line[32:48]
            tag = line[48:56]
            last_dw_be = line[56:60]
            first_dw_be = line[60:64]
            if (int(typ,2) == 4):            # for cfg
                completion_id = line[64:80]
                reserve_bit4 = line[80:84]       # reserved byte 10- bit 7:4
                ext_register_num = line[84:88]
                register_num = line[88:94]
                reserve_bit5 = line[94:96]       # reserved byte 11- bit 1:0
                payload = line[96:]
            elif(typ == '00000'):      # for memory
                addresses = line[64:94]
                reserve_bit4 = line[94:96] 
                payload = line[96:]
        		

            '''
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

            if((int(fmt,2)==0) and (int(typ,2)==0)): 
                 gen_f.write("Memory Read Request (MRd) with 3DW, no data           ")
                 gen_f.write("\n")
            if((int(fmt,2)==1) and (int(typ,2)==0)): 
                 gen_f.write("Memory Read Request (MRd) with 4DW, no data           ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==0) and (int(typ,2)==1)): 
                 gen_f.write("Memory Read Lock Request (MRdLk) with 3DW, no data     ")
                 gen_f.write("\n")
            if((int(fmt,2)==1) and (int(typ,2)==1)): 
                 gen_f.write("Memory Read Lock Request (MRdLk) with 4DW, no data     ")
                 gen_f.write("\n")
                              
            if((int(fmt,2)==2) and (int(typ,2)==0)): 
                 gen_f.write("Memory Write Request (MWr) with 3DW, with data         ")
                 gen_f.write("\n")
            if((int(fmt,2)==3) and (int(typ,2)==0)): 
                 gen_f.write("Memory Write Request (MWr) with 4DW, with data         ")
                 gen_f.write("\n")
                
            if((int(fmt,2)==0) and (int(typ,2)==2)): 
                 gen_f.write("IO Read Request (IORd) with 3DW, no data               ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==2)): 
                 gen_f.write("IO Write Request (IOWr) with 3DW, with data    ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==0) and (int(typ,2)==4)): 
                 gen_f.write("Config Type 0 Read Request (CfgRd0) with 3DW, no data")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==4)): 
                 gen_f.write("Config Type 0 Write Request (CfgWr0) with 3DW, with data")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==0) and (int(typ,2)==5)): 
                 gen_f.write("Config Type 1 Read Request (CfgRd1) with 3DW, no data")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==5)): 
                 gen_f.write("Config Type 1 Write Request (CfgWr1) with 3DW, with data")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==1) and (int(typ,2)==2)): 
                 gen_f.write("Message Request (Msg) with 4DW, no data              ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==3) and (int(typ,2)==2)): 
                 gen_f.write("Message Request W/Data (MsgD) with 4DW, with data      ")
                 gen_f.write("\n")
                 
                 
            if((int(fmt,2)==0) and (int(typ,2)==10)): 
                 gen_f.write("Completion (Cpl) with 3DW, no data                   ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==10)): 
                 gen_f.write("Completion W/Data (CpID) with 3DW, with data           ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==0) and (int(typ,2)==11)): 
                 gen_f.write("Completion-Locked (CpILk) with 3DW, no data          ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==11)): 
                 gen_f.write("Completion W/Data (CplDLk) with 3DW, with data         ")
                 gen_f.write("\n")
                 
            if((int(fmt,2)==2) and (int(typ,2)==12)): 
                 gen_f.write("Fetch and Add AtomicOp Request with 3DW, with data     ")
                 gen_f.write("\n")
            if((int(fmt,2)==3) and (int(typ,2)==12)): 
                 gen_f.write("Fetch and Add AtomicOp Request with 3DW, with data     ")
                 gen_f.write("\n")
            
 
            gen_f.write("fmt = ")
            gen_f.write(str(hex(int(fmt,2))))
            gen_f.write("\n")
            gen_f.write("typ = ")
            gen_f.write(str(hex(int(typ,2))))
            gen_f.write("\n")
            gen_f.write("reserve_bit1 = ")
            gen_f.write(str(hex(int(reserve_bit1,2))))
            gen_f.write("\n")
            gen_f.write("tc = ")
            gen_f.write(str(hex(int(tc,2))))
            gen_f.write("\n")
            gen_f.write("reserve_bit2 = ")
            gen_f.write(str(hex(int(reserve_bit2,2))))
            gen_f.write("\n")
            gen_f.write("attr1 = ")
            gen_f.write(str(hex(int(attr1,2))))
            gen_f.write("\n")
            gen_f.write("reserve_bit3 = ")
            gen_f.write(str(hex(int(reserve_bit3,2))))
            gen_f.write("\n")
            gen_f.write("th = ")  
            gen_f.write(str(hex(int(th,2))))
            gen_f.write("\n")
            gen_f.write("td = ")  
            gen_f.write(str(hex(int(td,2))))
            gen_f.write("\n")
            gen_f.write("ep = ") 
            gen_f.write(str(hex(int(ep,2))))
            gen_f.write("\n")
            gen_f.write("attr0 = ")
            gen_f.write(str(hex(int(attr0,2))))
            gen_f.write("\n")
            gen_f.write("at = ")
            gen_f.write(str(hex(int(at,2))))
            gen_f.write("\n")
            gen_f.write("length = ")
            gen_f.write(str(hex(int(length,2))))
            gen_f.write("\n")
            gen_f.write("requester_id = ")
            gen_f.write(str(hex(int(requester_id,2))))
            gen_f.write("\n")
            gen_f.write("tag = ")
            gen_f.write(str(hex(int(tag,2))))

            gen_f.write("\n")
            gen_f.write("last_dw_be = ")
            gen_f.write(str(hex(int(last_dw_be,2))))
            gen_f.write("\n")
            gen_f.write("first_dw_be = ")
            gen_f.write(str(hex(int(first_dw_be,2))))
            gen_f.write("\n")
            #gen_f.write("reserve_bit4 = ")
            #gen_f.write(str(hex(int(reserve_bit4,2))))
            #gen_f.write("\n")
            print(reserve_bit4)
            
            if (typ[2] == '1'):            # for cfg
                gen_f.write("Completion_Id  = ")
                gen_f.write(str(hex(int(completion_id,2))))
                gen_f.write("\n")
                gen_f.write("Rsv_10_7  = ")
                gen_f.write(str(hex(int(reserve_bit4,2))))
                gen_f.write("\n")
                gen_f.write("Ext_Register_Num  = ")
                gen_f.write(str(hex(int(ext_register_num,2))))
                gen_f.write("\n")
                gen_f.write("Register_Num  = ")
                gen_f.write(str(hex(int(register_num,2))))
                gen_f.write("\n")
                gen_f.write("Rsv_11_1  = ")
                gen_f.write(str(hex(int(reserve_bit5,2))))
                gen_f.write("\n")
                gen_f.write("payload = ")
                gen_f.write(str(hex(int(payload,2))))
                gen_f.write("\n")
            elif(int(typ,2) == 0):      # for memory
                gen_f.write("Address  = ")
                gen_f.write(str(hex(int(addresses,2))))
                gen_f.write("\n")
                #gen_f.write("Rsv_11_1  = ")
                #gen_f.write(str(hex(int(reserve_bit4,2))))
                #gen_f.write("\n")
                gen_f.write("payload = ")
                gen_f.write(str(hex(int(payload,2))))
                gen_f.write("\n")
			

            self.tx_no=self.tx_no+1
        bin_f.close()

      
