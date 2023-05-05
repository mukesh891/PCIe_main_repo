import random
from pprint import pprint

from pcie_seq_tlp_item_base_pkg import *
from pcie_com_file import *
import queue
print("hello pcie_seq_config_pkg")
f = open("hex_file.txt","w")
class pcie_seq_rc_config_pkt(pcie_pkg):
    def __init__(self):
        self.num_pkts=argv.num_pkts        
        self.err_eij = argv.err_eij
        self.err_pkt_no = argv.err_pkt_no
        self.arr_t =[0]*self.err_pkt_no
        for i in range(self.err_pkt_no):
            self.arr_t[i] = random.randrange(self.num_pkts)
        self.arr = list(set(self.arr_t))
        self.arr.sort()
        print(self.arr)
        print(self.num_pkts)
        self.k=0
        self.j=0
        super().__init__()
    def cfg0_pkt(self):
        self.fmt                    = random.choice([0,2])
        ##    BDF format for requester and completer    ##
        self.requester_id           = random.getrandbits(16)
        self.completer_id           = random.getrandbits(16)
        self.completer_id           = 0 
        ##################################################
        self.type                   = random.choice([4,5])
        self.first_dw_be            = 0b0011
        self.ep                     = 0 
        self.td                     = 0
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
        self.register_number        = random.choice([0,63])


    def bad_pkt_eij(self):
        self.fmt                    = random.choice([1,3,4,5,6,7])

    '''def mix_pkt(self):
        arr=[0]*20
        for i in range(20):
            arr[i] = random.randrange(0,100)
            print(arr[i])
    '''
    def fmt_eij_err(self):
        for i in range(self.num_pkts):
            for i in self.arr:
                self.bad_pkt_eij()


    def print_f(self):
        pprint(vars(self))
    def bin_file_handle(self):
        bin_f = open("bin_file.txt","w")
        self.k=self.k+1
        #self.cfg0_pkt()
        ## converting all the values to bin format ##
        if(self.err_eij):
            if (self.arr[self.j]==self.k and self.j < len(self.arr)-1):
                self.fmt_eij_err()
                print(self.fmt)
                self.j=self.j+1
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
        str(completer_id_str)+
        str(reserve_bit4_str)+
        str(ext_register_number_str)+
        str(register_number_str)+
        str(reserve_bit5_str)+
        str(payload_str))
        ##################################################################################
        
        ## puting the tlp_packet into queue ##
        pkt_queue.put(tlp_packet)
        #print(pkt)
        ## Writing the tlp_packet into the hex_fil.txt ##
        bin_f.write(tlp_packet)
        bin_f.write("\n")
        bin_f.close()
        
    def hex_file_handle(self):
        bin_f = open("/home/mukesh/PCIe/PCIe_repo/src/rc_src/bin_file.txt","r")
        hex_f = open("/home/mukesh/PCIe/PCIe_repo/src/rc_src/hex_file.txt","w")
        for line in bin_f:
            line = "0b" + line
            hex_val = hex(int(line,2))[2:]
            print(hex_val)
            hex_f.write(hex_val)
            hex_f.write("\n")
        hex_f.close()
        bin_f.close()


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
            #fmt_hex = hex(self.fmt)       
            #requester_id_hex        = hex(self.requester_id) 
            #completer_id_hex        = hex(self.completer_id)
            #type_hex                = hex(self.type)      
            #first_dw_be_hex         = hex(self.first_dw_be)
            #ep_hex                  = hex(self.ep)        
            #td_hex                  = hex(self.td)        
            #tc_hex                  = hex(self.tc)        
            #attr0_hex               = hex(self.attr0)
            #attr1_hex               = hex(self.attr1)
            #at_hex                  = hex(self.at)
            #length_hex              = hex(self.length)
            #tag_hex                 = hex(self.tag)
            #last_dw_be_hex          = hex(self.last_dw_be)
            #reserve_bit4_hex        = hex(self.reserve_bit4)
            #ext_register_number_hex = hex(self.ext_register_number)
            #register_number_hex     = hex(self.register_number)
            #reserve_bit5_hex        = hex(self.reserve_bit5)
            #payload_hex             = hex(self.payload)           
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


        self.hex_file_handle


c = pcie_seq_rc_config_pkt()
#c.bin_file_handle()
#c.file_handle()
#c.hex_file_handle()
#c.mix_pkt()
c.gen_log()

