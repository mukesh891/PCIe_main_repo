import os,queue
import argparse
import random 
cwd = os.getcwd()
class pcie_config_obj:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--num_pkts', type= int , help = 'Total num of packets to be generated at generator side and must be positive value', default = 100)
        parser.add_argument('--err_eij', type= int , help = 'A bit value to represent error injection is done or not and must be 0,1', default = 0)
        parser.add_argument('--err_pkt_no', type= int , help = 'Total no. of error pkt to be injected', default = 0)
        
        return parser.parse_args()
c=pcie_config_obj
argv = pcie_config_obj.parse_args()
err_eij = argv.err_eij
err_pkt_no = argv.err_pkt_no 
num_pkts= argv.num_pkts
pkt_queue = queue.Queue()
arr = []
compl_pkt_queue = queue.Queue()
if(err_eij): 
    while len(arr) < err_pkt_no:
        num = random.randrange(0,num_pkts-1)
        if num not in arr:
            arr.append(num)
        arr.sort()
print(len(arr))
print(arr)
print(num_pkts)
	

