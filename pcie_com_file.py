import os,queue
import argparse
import random 
import logging
import datetime
import inspect
current_datetime = datetime.datetime.now()
file_path = inspect.currentframe().f_code.co_filename
line_no = inspect.currentframe().f_lineno
file_name = os.path.basename(file_path)

formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
formatted_datetime = f"{formatted_dt} \t"#- {file_name}:{line_no}"
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
        parser.add_argument('--test', type= str , help = 'Total no. of error pkt to be injected in completer', default = 'cfg_test')
        parser.add_argument('--num_ep_pkt_tx', type= int , help = 'Total number of packets generated from end-point', default = 0)
        parser.add_argument('--DW', type= int , help = 'Maximum payload size to be sent', default = 1,choices=range(1,1024))
        parser.add_argument('--mps', type= int , help = 'Maximum payload size to be sent', default = 3,choices=range(1,20))
        parser.add_argument('--delay_en', type= int , help = 'Total no. of error pkt to be injected in completer', default = 0)
        parser.add_argument('--RCB64_en', type= bool , help = 'for enabling RCB to read 64 bytes at 1 time', default = 1)
        parser.add_argument('--RCB128_en', type= bool , help = 'for enabling RCB to read 128 bytes at 1 time', default = 0)


        return parser.parse_args()
c=pcie_config_obj
argv = pcie_config_obj.parse_args()
err_eij = argv.err_eij
err_pkt_no = argv.err_pkt_no 
num_pkts= argv.num_pkts

ep_err_eij = argv.ep_err_eij
ep_err_pkt_no = argv.ep_err_pkt_no 
test = argv.test
num_ep_pkt_tx = argv.num_ep_pkt_tx
DW = argv.DW
mps = argv.mps
delay_en= argv.delay_en
RCB64_en = argv.RCB64_en
RCB128_en = argv.RCB128_en
pkt_queue = queue.Queue()
seq_tx_no = 0

compl_pkt_queue = queue.Queue()
fixed_ecrc_divisor = '10101010101010101010101010101010'


if(err_pkt_no > num_pkts):
    logger.fatal("err_pkt_no cannot be grater than num_pkts")
    sys.exit()
if(ep_err_pkt_no > num_pkts):
    logger.fatal("err_pkt_no cannot be grater than num_pkts")
    sys.exit()

