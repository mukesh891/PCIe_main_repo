import os,queue
import argparse
import random,logging 
from pcie_com_file import *
cwd = os.getcwd()
g_pkt_queue = queue.Queue()
seq_tx_no = 0
logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_com_file.py file")

arr = []
if(err_eij): 
    while len(arr) < err_pkt_no:
        num = random.randrange(0,num_pkts-1)
        if num not in arr:
            arr.append(num)
        arr.sort()
#print(len(arr))
#print(arr)
#print(num_pkts)
	

