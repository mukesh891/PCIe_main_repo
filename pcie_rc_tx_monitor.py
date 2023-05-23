from tabulate import tabulate
from pcie_lib import *
#err_id_f = open("gen_logs/error_id_file.txt","w") 
#bin_file = open("gen_logs/bin_file.txt","r") 
#err_bin_file = open("gen_logs/err_bin_file.txt","w")

rc_monitor_f=open("gen_logs/rc_tx_good_monitor_log.txt","w")
rc_mixed_monitor_f=open("gen_logs/rc_tx_mixed_monitor_log.txt","w")
class pcie_rc_tx_monitor:
    def pcie_rc_gen_monitor(self):
        bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r")
        self.i=0
        for line in bin_f:
        #line = "00000100000000000000000000000001000001011100001001011000000000110000000000000000000000001111000000000000000000000000000000000000"
            rc_monitor_f.write("------------------------------------------------------------------- TLP ")
            rc_monitor_f.write(str(self.i))
            rc_monitor_f.write("---------------------------------------------------------------------------------------- ")
            Fmt = line[0:3]
            Type = line[3:8]
            T9 = line[8]
            TC = line[9:12]
            T8 = line[12]
            Attr1 = line[13]
            LN = line[14]
            TH = line[15]
            TD = line[16]
            EP = line[17]
            Attr0 = line[18:20]
            AT = line[20:22]
            Length = line[22:32]
            #if Fmt == '010' or Fmt=='000' and Typ == '00100':
            #	print("Its a config request")
            #if Fmt == '010' or Fmt=='000' and Typ == '00000':
            #	print("Its a Memory Request")
            Requester_Id = line[32:48]
            Tag = line[48:56]
            Last_DW_BE = line[56:60]
            First_DW_BE = line[60:64]
            if (Type[2] == '1'): # for cfg
                Completion_Id = line[64:80]
                Rsv_10_7 = line[80:84] # reserved byte 10- bit 7:4
                Ext_Register_Num = line[84:88]
                Register_Num = line[88:94]
                Rsv_11_1 = line[94:96] # reserved byte 11- bit 1:0
            elif(Type[:-1] == '0000'): # for memo
                Address = line[64:94]
                Rsv_11_1 = line[94:96]
            
            
            
            Header = line[0:96]
            Data = line[96:]
            #data_size = len(line[96:])
            
            #if((int(Fmt[1], 2) == 1) | (int(temp_valid_pkts[-1], 2) != 0)):  # data will be zero if either packet is invalid or config write line
                	#	data = 0
                	#	line = line + format(data, data_size)
            #else:                                                     # else data is sent 
                	#	data = int(data_from_cfg, 2)
            #line = line + format(data, data_size)
            data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Completion_Id, Rsv_10_7,Ext_Register_Num, Rsv_11_1, Header, Data]] 
            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id', 'Rsv_10_7', 'Ext_Register_Num', 'Register_Num', 'Rsv_11_1', 'Header', 'Data']
                	
            table = tabulate(data, headers=headers, tablefmt='orgtbl')
            rc_monitor_f.write(table)
            rc_monitor_f.write("\n")
            self.i=self.i+1
        bin_f.close()

    def pcie_rc_driver_monitor(self):
        mixed_bin_f = open("gen_logs/rc_tx_mixed_bin_file.txt","r")
        self.i=0
        for line in mixed_bin_f:
        #line = "00000100000000000000000000000001000001011100001001011000000000110000000000000000000000001111000000000000000000000000000000000000"
            rc_mixed_monitor_f.write("------------------------------------------------------------------- TLP ")
            rc_mixed_monitor_f.write(str(self.i))
            rc_mixed_monitor_f.write("---------------------------------------------------------------------------------------- ")
            Fmt = line[0:3]
            Type = line[3:8]
            T9 = line[8]
            TC = line[9:12]
            T8 = line[12]
            Attr1 = line[13]
            LN = line[14]
            TH = line[15]
            TD = line[16]
            EP = line[17]
            Attr0 = line[18:20]
            AT = line[20:22]
            Length = line[22:32]
            #if Fmt == '010' or Fmt=='000' and Typ == '00100':
            #	print("Its a config request")
            #if Fmt == '010' or Fmt=='000' and Typ == '00000':
            #	print("Its a Memory Request")
            Requester_Id = line[32:48]
            Tag = line[48:56]
            Last_DW_BE = line[56:60]
            First_DW_BE = line[60:64]
            if (Type[2] == '1'): # for cfg
                Completion_Id = line[64:80]
                Rsv_10_7 = line[80:84] # reserved byte 10- bit 7:4
                Ext_Register_Num = line[84:88]
                Register_Num = line[88:94]
                Rsv_11_1 = line[94:96] # reserved byte 11- bit 1:0
            elif(Type[:-1] == '0000'): # for memo
                Address = line[64:94]
                Rsv_11_1 = line[94:96]
            
            
            
            Header = line[0:96]
            Data = line[96:]
            #data_size = len(line[96:])
            data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Completion_Id, Rsv_10_7,Ext_Register_Num, Rsv_11_1, Header, Data]] 
            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id', 'Rsv_10_7', 'Ext_Register_Num', 'Register_Num', 'Rsv_11_1', 'Header', 'Data']
                	
            table = tabulate(data, headers=headers, tablefmt='orgtbl')
            rc_mixed_monitor_f.write(table)
            rc_mixed_monitor_f.write("\n")
            rc_mixed_monitor_f.write("\n")
            self.i=self.i+1
        mixed_bin_f.close()

gen_mon = pcie_rc_tx_monitor()
gen_mon.pcie_rc_gen_monitor()
gen_mon.pcie_rc_driver_monitor()
rc_monitor_f.close()
rc_mixed_monitor_f.close()
