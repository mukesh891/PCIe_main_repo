from pcie_com_file import *
from pcie_ep_field_fn import *
import random



pkt_valid_queue = queue.Queue()
#//////////////////////////////////////////
#compl_qsize = pkt_valid_queue.qsize()
#print('complqsize is {}'.format(compl_qsize))

'''lines = open("ep_logs/binary_completer.txt","r")
line_count = 0
for i in lines:
            line_count = line_count + 1
lines.close()
            


ep_err_arr = []
if(ep_err_eij): 
    while len(ep_err_arr) < ep_err_pkt_no:
        num = random.randrange(0,line_count)
        #err_bin_compl.write('giving error {}, total pkts {}\n'.format(num, num_pkts))
        if num not in ep_err_arr:
            ep_err_arr.append(num)
            error.write('Injecting error in pkt number {}, total pkts {}\n'.format(num, line_count))
        ep_err_arr.sort()
error.write('print the error list {}\n'.format(ep_err_arr))'''
