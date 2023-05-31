from tabulate import tabulate
from pcie_lib import *
from pcie_com_file import *
#err_id_f = open("gen_logs/error_id_file.txt","w") 
#bin_file = open("gen_logs/bin_file.txt","r") 
#err_bin_file = open("gen_logs/err_bin_file.txt","w")
logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_tx_monitor.py file")

rc_monitor_f=open("gen_logs/mon_logs/rc_tx_good_monitor_log.txt","w")
rc_mixed_monitor_f=open("gen_logs/mon_logs/rc_tx_mixed_monitor_log.txt","w")
class pcie_rc_tx_monitor:
    def pcie_rc_gen_monitor(self):
        bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r")
        self.i=0
        for line in bin_f:
        #line = "00000100000000000000000000000001000001011100001001011000000000110000000000000000000000001111000000000000000000000000000000000000"
            #rc_monitor_f.write("\n")
            #rc_monitor_f.write("\n")
            rc_monitor_f.write("\n\n------------------------------------------------------------------- TLP ")
            rc_monitor_f.write(str(self.i))
            rc_monitor_f.write("----------------------------------------------------------------------------------------\n ")
            #rc_monitor_f.write("\n")
            #rc_monitor_f.write("\n")
            rc_monitor_f.write("\n")
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
            elif(Type == '00000'): # for memo
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
            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id', 'Rsv_10_7', 'Ext_Register_Num', 'Register_Num', 'Rsv_11_1', 'Header', 'Data']
            if (Type[2] == '1'): # for cfg
                data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Completion_Id, Rsv_10_7,Ext_Register_Num, Rsv_11_1, Header, Data]] 
            elif(Type == '00000'): # for memo
                data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Address, Rsv_11_1, Header, Data]] 
                	
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
            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id', 'Rsv_10_7', 'Ext_Register_Num', 'Register_Num', 'Rsv_11_1', 'Header', 'Data']
            if (Type[2] == '1'): # for cfg
                data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Completion_Id, Rsv_10_7,Ext_Register_Num, Rsv_11_1, Header, Data]] 
                table = tabulate(data, headers=headers, tablefmt='orgtbl')
                rc_mixed_monitor_f.write(table)
            elif(Type == '00000'): # for memo
                data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id,Tag,Last_DW_BE, First_DW_BE, Address, Rsv_11_1, Header, Data]] 
                table = tabulate(data, headers=headers, tablefmt='orgtbl')
                rc_mixed_monitor_f.write(table)
                
                	
            rc_mixed_monitor_f.write("\n")
            rc_mixed_monitor_f.write("\n")
            self.i=self.i+1
        mixed_bin_f.close()

    def compare_files(self,file1_path, file2_path, output_file_path):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_file_path, 'w') as output_file:
            #for line1 in file1,line2 in file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            lines3 = file2.readlines()
            #lines3 = output_file.writelines()
            # Find the number of matching lines
            num_matched_lines = sum(1 for line1, line2 in zip(lines1, lines2) if line1 == line2)
            num_not_matched_lines=sum(1 for line1, line2 in zip(lines1, lines2) if line1 != line2)
            # Write the lines with comments to the output file
            for line1, line2 in zip(lines1, lines2):
            #for line1 in file1 and line2 in file2:
                    if line1 == line2:
                        output_file.write(f"# Received: {num_matched_lines}\t{line1}") #output_file.write(f"# Received: {num_matched_lines}\t{line1}")
                    else:
                        output_file.write(f"# not Received: {num_not_matched_lines}\n (RC_SIDE packet send)\t {line1} (EP_SIDE packet recv)\t {line2} \n {lines3}")
                        #output_file.write(lines2)
        
# Example path
file1_path = 'gen_logs/rc_tx_mixed_bin_file.txt'
file2_path = 'ep_logs/binary_completer.txt'
output_file_path = 'gen_logs/mon_logs/mon_received_file.txt'



gen_mon = pcie_rc_tx_monitor()
gen_mon.pcie_rc_gen_monitor()
gen_mon.pcie_rc_driver_monitor()
gen_mon.compare_files(file1_path, file2_path, output_file_path)
logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Generating gen_logs/mon_logs/rc_tx_good_monitor_log.txt log")
rc_monitor_f.close()
logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Generating gen_logs/mon_logs/rc_tx_mixed_monitor_log.txt log")
rc_mixed_monitor_f.close()
