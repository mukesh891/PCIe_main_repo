from pcie_com_file import *
import random
import re
mem_queue = {}
RC_BASE_ADDR = 0x10000
EP_BASE_ADDR = 0x100000
MAX_PAYLOAD = 32 # 3DW
## 256kb of configuration space ##
CFG_SPACE = 256 * 2**3
# Define the queue as a dictionary with offset addresses as keys and values as lists of random data

logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_memory_space.py file")

def memory_space():
    ## Note : to open the rc_rx_good_bin_file.txt in read format to get the payload to be written to ep memory
    bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r")
    ## Note : Write the rc memory space for completion check 
    mem_f = open("gen_logs/rc_memory.txt","w")
    for line in bin_f:  # range for 1kb addr offset
        line = line.strip('\n')        
        if((line[:3] == '010') and (line[3:8] == '00000')) or ((line[:3] in ['000','010']) and (line[3:8] in '00100')):
            offset = line[89:94]
            first_dw_be = line[60:64]
            data0 = line[96:]
            
            for i in range(0,(int(len(data0))//int(MAX_PAYLOAD))):
                data = int(data0,2)
                byte1 = data  & 0xFF
                byte2 = data  & 0x0000FF00
                byte3 = data  & 0x00FF0000
                byte4 = data  & 0xFF000000
                
                ## Note : Getting payload according to first_dw_be 
                if first_dw_be == "0000": 
                    data = format(0,'032b')
                elif first_dw_be == "0001":
                    data = byte1 
                    data = format(0,'032b')
                elif first_dw_be == "0010":
                    data = byte2 
                elif first_dw_be == "0011":
                    data = byte1 + byte2 
                elif first_dw_be == "0100":
                    data = byte3
                elif first_dw_be == "0101":
                    data = byte1 + byte3 
                elif first_dw_be == "0110":
                    data = byte2 + byte3 
                elif first_dw_be == "0111":
                    data = byte1 + byte2 + byte3 
                elif first_dw_be == "1000":
                    data = byte4
                elif first_dw_be == "1001":
                    data = byte4 + byte1 
                elif first_dw_be == "1010":
                    data = byte4 + byte3 
                elif first_dw_be == "1011":
                    data = byte4 + byte1 + byte2 
                elif first_dw_be == "1100":
                    data = byte4 + byte3
                elif first_dw_be == "1101":
                    data = byte4 + byte3 +byte1  
                elif first_dw_be == "1110":
                    data = byte4 + byte3 +byte2  
                elif first_dw_be == "1111":
                    data = byte4 + byte3 +byte2 +byte1 
                '''
                if int(first_dw_be,2) >0 :
                    offset = offset+'00'
                elif int(first_dw_be,2) >=2 :
                    offset = offset+'01'
                elif int(first_dw_be,2) >=4 :
                    offset = offset+'10'
                elif int(first_dw_be,2) ==8 :
                    offset = offset+'11'
                '''
                data = '0X'+'{:08X}'.format(data)
                offset_hex = (hex(int(offset,2)).upper())
                mem_queue[offset] = data
                mem_f.write(f"Offset: {offset_hex}\t Data: {data}")
                mem_f.write("\n")
    mem_f.close()
    bin_f.close()

memory_space()

def completion_data():
    com_bin_f = open("ep_logs/binary_completer.txt","r")
    mem_f = open("gen_logs/rc_memory.txt","r")
    com_mem_f = open("gen_logs/compl_mem_match.txt","w")
    for line in com_bin_f:  # range for 1kb addr offset
        line = line.strip('\n')        
        data0 = line[96:]

        data = int(data0,2)
        data = '0X'+'{:08X}'.format(data)
        for l in mem_f:
            data_search = r'Data:\s*(0X[0-9A-F]+)'
            data_pat = re.search(data_search,l)
            if data_pat:
                com_mem_f.write(f"Data Matched : {data}")
                com_mem_f.write("\n")
                break

        mem_f.seek(0)
    com_mem_f.close()
    com_bin_f.close()

completion_data()



