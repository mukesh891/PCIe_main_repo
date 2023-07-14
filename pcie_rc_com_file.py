import os,queue
import argparse
import random 
from pcie_com_file import *
from pcie_lib import *
cwd = os.getcwd()
g_pkt_queue = queue.Queue()
seq_tx_no = 0
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_com_file.py file")

rc_error_count_for_write_mem = 0
rc_error_count_for_read_mem = 0
ep_to_rc_err_eij_arr = []

packet_numbers = 0

ep_good_pkts_rcvd = []
ep_bad_pkts_rcvd = []
#arr = []
#if(err_eij): 
#    while len(arr) < err_pkt_no:
#        num = random.randrange(0,num_pkts-1)
#        if num not in arr:
#            arr.append(num)
#        arr.sort()
#print(len(arr))
#print(arr)
#print(num_pkts)
	

