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
        parser.add_argument('--ep_err_eij', type= int , help = 'A bit value to represent error injection is done from EP completer', default = 0)
        parser.add_argument('--ep_err_pkt_no', type= int , help = 'Total no. of error pkt to be injected in completer', default = 0)
        parser.add_argument('--test', type= str , help = 'Total no. of error pkt to be injected in completer', default = 'cfg_seq_test')
        
        return parser.parse_args()
c=pcie_config_obj
argv = pcie_config_obj.parse_args()
err_eij = argv.err_eij
err_pkt_no = argv.err_pkt_no 
num_pkts= argv.num_pkts

ep_err_eij = argv.ep_err_eij
ep_err_pkt_no = argv.ep_err_pkt_no 
test = argv.test


pkt_queue = queue.Queue()
seq_tx_no = 0

compl_pkt_queue = queue.Queue()
	

