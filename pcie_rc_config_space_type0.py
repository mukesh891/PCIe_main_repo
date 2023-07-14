import random
from pcie_com_file import *
from pcie_rc_com_file import *
from tabulate import tabulate
from array import array
import logging

#rcvd_pkts_from_ep = open("gen_logs/rc_ep_side_pkt_recieved_memory.txt","r")
with open("gen_logs/rc_config_space.txt","w") as fil:
    print("Hello Config space")
if RCB64_en and ~RCB128_en:
    RCB = 16 #dw i.e 64 bytes

if RCB128_en and ~RCB64_en:
    RCB = 32 #dw i.e 128 bytes

class rc_cfg_space_type0():
    def __init__(self):
        self.cfg_array = array('Q', [0] * 16)
        self.Max_Lat = format(0, '08b')
        self.Min_Gnt = format(0, '08b')
        self.Interrupt_Pin = format(0, '08b')
        self.Interrupt_Line = format(0, '08b')
        self.Reserved1 = format(1, '032b')
        self.Capability_Pointer = format(0b10101100, '08b')
        self.Reserved0 = format(0, '024b')
        self.Expansion_ROM_Base_Address = format(0xa0f00,'032b')
        self.Subsystem_Device_ID = format(2, '016b')
        self.Subsystem_Vendor_ID = format(540, '016b')
        self.CardBus_CIS_Pointer = format(1, '032b')
        self.BAR5 = format(0xffffffff, '032b')
        self.BAR4 = format(0xffffffff, '032b')
        self.BAR3 = format(0xffffffff, '032b')
        self.BAR2 = format(0xffffffff, '032b')
        self.BAR1 = format(0xffffffff, '032b')
        self.BAR0 = format(0xffffffff, '032b')
        self.BIST = format(0, '08b')
        self.Header_Type = format(0b00000000, '08b')
        self.Latency_Timer = format(0, '08b')
        self.Cache_line_Size = format(64, '08b')
        self.Class_Code = format(0, '024b')
        self.Rev_ID = format(1, '08b')
        self.Status = format(0b10000, '016b')
        self.Command = format(0b110, '016b')
        self.Device_ID = format(2, '016b')
        self.Vendor_ID = format(540, '016b')

    #def initial_cfg_func(self):
    #    self.type_0_header = self.Vendor_ID + self.Device_ID + self.Command + self.Status + self.Rev_ID + self.Class_Code + self.Cache_line_Size + self.Latency_Timer + self.Header_Type + self.BIST + self.BAR0 + self.BAR1 + self.BAR2 + self.BAR3 + self.BAR4 + self.BAR5 + self.CardBus_CIS_Pointer + self.Subsystem_Vendor_ID + self.Subsystem_Device_ID + self.Expansion_ROM_Base_Address + self.Capability_Pointer + self.Reserved0 + self.Reserved1 + self.Interrupt_Line + self.Interrupt_Pin + self.Min_Gnt + self.Max_Lat

    def rc_config_space_func(self, ep_queue, pkt_num, data_rcvd, compl_st):
        rc_cfg = open("gen_logs/rc_config_space.txt","a")

        data_rcvd = str(data_rcvd)
        #valid_pkts =  rcvd_pkts_from_ep.readline()
        valid_pkts = ep_queue 
        rc_cfg.write("--- pkt recieved {}---".format(valid_pkts))
        

        if int(compl_st, 2) == 0:
            rc_cfg.write("-------------- compl status passed ----------- ")
            compl_code = format(0, '04b')
        else:
            rc_cfg.write("-------------- compl code  status also passed ----------- ")
            compl_code = format(int(compl_st, 2), '04b')
        Bist = '1' + '0' + '00' + compl_code
        self.BIST = format(int(Bist, 2), '08b')

        self.cfg_array[3] = int(self.BIST + self.Header_Type + self.Latency_Timer + self.Cache_line_Size, 2)

        data_sent = format(0, '032b')
        rc_cfg.write("-------------- no error flat 1----------- ")

        if int(compl_code, 2) == 0:
            rc_cfg.write("-------------- no error flat 2----------- ")
            if valid_pkts[1] =='1':
                logging.info("-------------- no error flat 4----------- ")
                data_sent = format(0, '032b')
                self.write_addr = pkt_num % 1
                if self.write_addr == 0:
                    if data_rcvd is not None:
                        rc_cfg.write("\ndata recieved -> {}\n".format(data_rcvd))
                        self.cfg_array[4] = int(data_rcvd, 2) & 0xFFFFFF00
                    else:
                        self.cfg_array[4] = self.cfg_array[4]
            elif valid_pkts[1] == '0':
                rc_cfg.write("-------------- no error flat 3----------- ")
                self.read_addr = pkt_num % 16
                data_sent = format(self.cfg_array[self.read_addr], '032b')
                rc_cfg.write("read adder ----->{}".format(self.read_addr))
            
        else:
            data_sent = format(0, '032b')

        self.type_0_header = format(self.cfg_array[0], '032b') + format(self.cfg_array[1], '032b') + format(self.cfg_array[2], '032b') + format(self.cfg_array[3], '032b') + format(self.cfg_array[4], '032b') + format(self.cfg_array[5], '032b') + format(self.cfg_array[6], '032b') + format(self.cfg_array[7], '032b') + format(self.cfg_array[8], '032b') + format(self.cfg_array[9], '032b') + format(self.cfg_array[10], '032b') + format(self.cfg_array[11], '032b') + format(self.cfg_array[12], '032b') + format(self.cfg_array[13], '032b') + format(self.cfg_array[14], '032b') + format(self.cfg_array[15], '032b')
        table_data = [
        ("Vendor_ID",self.type_0_header[:16]),
        ("Device_ID",self.type_0_header[16:32]),
        ("Command",self.type_0_header[32:48]),
        ("Status",self.type_0_header[48:64]),
        ("Rev_ID",self.type_0_header[64:72]),
        ("Class_Code",self.type_0_header[72:96]),
        ("Cache_line_Size",self.type_0_header[96:104]),
        ("Latency_Timer",self.type_0_header[104:112]),
        ("Header_Type",self.type_0_header[112:120]),
        ("BIST",self.type_0_header[120:128]),
        ("BAR0",self.type_0_header[128:160]),
        ("BAR1",self.type_0_header[160:192]),
        ("BAR2",self.type_0_header[192:224]),
        ("BAR3",self.type_0_header[224:256]),
        ("BAR4",self.type_0_header[256:288]),
        ("BAR5",self.type_0_header[288:320]),
        ("CardBus_CIS_Pointer",self.type_0_header[320:352]),
        ("Subsystem_Vendor_ID",self.type_0_header[352:368]),
        ("Subsystem_Device_ID",self.type_0_header[368:384]),
        ("Expansion_ROM_Base_Address",self.type_0_header[384:416]),
        ("Capability_Pointer",self.type_0_header[416:424]),
        ("Reserved0",self.type_0_header[424:448]),
        ("Reserved1",self.type_0_header[448:480]),
        ("Interrupt_Line",self.type_0_header[480:488]),
        ("Interrupt_Pin",self.type_0_header[488:496]),
        ("Min_Gnt",self.type_0_header[496:504]),
        ("Max_Lat",self.type_0_header[504:512])                    
        ]
        # Print the table
        # print(tabulate(table_data, headers=["Field", "Value"], tablefmt="grid"))
        rc_cfg.write('\n-------> vendor id -> {}'.format(self.type_0_header[:16]))
        table = tabulate(table_data, headers=["Field", "Value"], tablefmt="grid")
        rc_cfg.write('\n\n printing type 0 header for packet {} \n\n' '{}\n'.format(pkt_num, table))
        rc_cfg.close()
        return data_sent

    def initial_cfg_func(self):
        rc_cfg = open("gen_logs/rc_config_space.txt","a")
        rc_cfg.write("rc_cfg_space_type0 block")

        self.cfg_array = array('Q', [0] * 16)

        type0header_size = '0' + str(16 * 32) + 'b'
        self.type_0_header = format(0, type0header_size)

        self.Vendor_ID = format(540, '016b')
        self.Device_ID = format(2, '016b')
        self.Command = format(0b110, '016b')
        self.Status = format(0b10000, '016b')
        self.Rev_ID = format(1, '08b')
        self.Class_Code = format(0, '024b')
        self.Cache_line_Size = format(64, '08b')
        self.Latency_Timer = format(0, '08b')
        self.Header_Type = format(0b00000000, '08b')
        self.BIST = format(0, '08b')
        self.BAR0 = format(0xffffffff, '032b')
        self.BAR1 = format(0xffffffff, '032b')
        self.BAR2 = format(0xffffffff, '032b')
        self.BAR3 = format(0xffffffff, '032b')
        self.BAR4 = format(0xffffffff, '032b')
        self.BAR5 = format(0xffffffff, '032b')
        self.CardBus_CIS_Pointer = format(1, '032b')
        self.Subsystem_Vendor_ID = format(540, '016b')
        self.Subsystem_Device_ID = format(2, '016b')
        self.Expansion_ROM_Base_Address = format(0xa0f00, '032b')
        self.Capability_Pointer = format(0b10101100, '08b')
        self.Reserved0 = format(0, '024b')
        self.Reserved1 = format(1, '032b')
        self.Interrupt_Line = format(0, '08b')
        self.Interrupt_Pin = format(0, '08b')
        self.Min_Gnt = format(0, '08b')
        self.Max_Lat = format(0, '08b')

        self.BAR0 = format((int(self.BAR0, 2) & 0xFFFFFF00), '032b')
        self.BAR1 = format((int(self.BAR1, 2) & 0xFFFFFC00), '032b')
        self.BAR2 = format((int(self.BAR2, 2) & 0xFFFFC000), '032b')
        self.BAR3 = format((int(self.BAR3, 2) & 0xFFFFFC00), '032b')
        self.BAR4 = format((int(self.BAR4, 2) & 0xFFFFC000), '032b')
        self.BAR5 = format((int(self.BAR5, 2) & 0xFFFFFF80), '032b')

        self.type_0_header = self.Vendor_ID + self.Device_ID + self.Command + self.Status + self.Rev_ID + self.Class_Code + self.Cache_line_Size + self.Latency_Timer + self.Header_Type + self.BIST + self.BAR0 + self.BAR1 + self.BAR2 + self.BAR3 + self.BAR4 + self.BAR5 + self.CardBus_CIS_Pointer + self.Subsystem_Vendor_ID + self.Subsystem_Device_ID + self.Expansion_ROM_Base_Address + self.Capability_Pointer + self.Reserved0 + self.Reserved1 + self.Interrupt_Line + self.Interrupt_Pin + self.Min_Gnt + self.Max_Lat

        rc_cfg.write('\n\n printing type 0 header \n\n' '{}\n'.format(self.type_0_header))
        table_data = [
        ("Vendor_ID",self.type_0_header[:16]),
        ("Device_ID",self.type_0_header[16:32]),
        ("Command",self.type_0_header[32:48]),
        ("Status",self.type_0_header[48:64]),
        ("Rev_ID",self.type_0_header[64:72]),
        ("Class_Code",self.type_0_header[72:96]),
        ("Cache_line_Size",self.type_0_header[96:104]),
        ("Latency_Timer",self.type_0_header[104:112]),
        ("Header_Type",self.type_0_header[112:120]),
        ("BIST",self.type_0_header[120:128]),
        ("BAR0",self.type_0_header[128:160]),
        ("BAR1",self.type_0_header[160:192]),
        ("BAR2",self.type_0_header[192:224]),
        ("BAR3",self.type_0_header[224:256]),
        ("BAR4",self.type_0_header[256:288]),
        ("BAR5",self.type_0_header[288:320]),
        ("CardBus_CIS_Pointer",self.type_0_header[320:352]),
        ("Subsystem_Vendor_ID",self.type_0_header[352:368]),
        ("Subsystem_Device_ID",self.type_0_header[368:384]),
        ("Expansion_ROM_Base_Address",self.type_0_header[384:416]),
        ("Capability_Pointer",self.type_0_header[416:424]),
        ("Reserved0",self.type_0_header[424:448]),
        ("Reserved1",self.type_0_header[448:480]),
        ("Interrupt_Line",self.type_0_header[480:488]),
        ("Interrupt_Pin",self.type_0_header[488:496]),
        ("Min_Gnt",self.type_0_header[496:504]),
        ("Max_Lat",self.type_0_header[504:512])
        ]
        table = tabulate(table_data, headers=["Field", "Value"], tablefmt="grid")
        rc_cfg.write('\n\n printing initial type 0 header \n\n' '{}\n'.format(table))

        self.cfg_array[0] = int(self.type_0_header[:32], 2)
        self.cfg_array[1] = int(self.type_0_header[32:64], 2)
        self.cfg_array[2] = int(self.type_0_header[64:96], 2)
        self.cfg_array[3] = int(self.type_0_header[96:128], 2)
        self.cfg_array[4] = int(self.type_0_header[128:160], 2)
        self.cfg_array[5] = int(self.type_0_header[160:192], 2)
        self.cfg_array[6] = int(self.type_0_header[192:224], 2)
        self.cfg_array[7] = int(self.type_0_header[224:256], 2)
        self.cfg_array[8] = int(self.type_0_header[256:288], 2)
        self.cfg_array[9] = int(self.type_0_header[288:320], 2)
        self.cfg_array[10] = int(self.type_0_header[320:352], 2)
        self.cfg_array[11] = int(self.type_0_header[352:384], 2)
        self.cfg_array[12] = int(self.type_0_header[384:416], 2)
        self.cfg_array[13] = int(self.type_0_header[416:448], 2)
        self.cfg_array[14] = int(self.type_0_header[448:480], 2)
        self.cfg_array[15] = int(self.type_0_header[480:512], 2)
        rc_cfg.close()


    def read_cfg(self,ep_queue ,data_rcvd, pkt_num, compl_st):
        self.rc_config_space_func(ep_queue,pkt_num, data_rcvd, compl_st)
        read_addr = self.read_addr
        if read_addr < 16:
            return format(self.cfg_array[read_addr], '032b')
        else:
            return format(0, '032b')

    def write_cfg(self,ep_queue ,data, pkt_num, compl_st):
        self.rc_config_space_func(ep_queue,pkt_num, data, compl_st)
        data = int(str(data),2)
        write_addr = int(str(self.write_addr),) #int(addr, 2)
        if write_addr < 16:
            self.cfg_array[write_addr] = data

        print(self.cfg_array[write_addr])

cls=rc_cfg_space_type0()
cls.initial_cfg_func()
##cls.rc_config_space_func(pkt_num, data_rcvd, compl_st)
#cls.rc_config_space_func(0,101010,'0')
#cls.write_cfg(10,10110)
#read_data = cls.read_cfg(10)
#print(read_data)
