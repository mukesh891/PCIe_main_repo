import random, time
import console_to_log
#from pkt_dict import *
from pcie_com_file import *
from pcie_ep_com_file import *

# Redirect console output to a log file
console_to_log.redirect_output_to_file()
print("ep_base_pkt block")
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_base.py file")


class ep_base_pkt():
	def __init__(self):
		Fmt = 0		
		Type = 0
		T9 = 0
		TC = 0
		T8 = 0
		Attr1 = 0
		LN = 0
		TH = 0
		TD = 0
		EP = 0
		Attr0 = 0
		AT = 0
		Length = 0

		Requester_Id = 0
		Tag = 0
		Last_DW_BE = 0
		First_DW_BE = 0	
	
	def checker_fn_base(pkt_num):
		
		TLP = format(0, '0128b')   #default set
		#TLP = pkt_queue.queue[pkt_num]
		'''while pkt_queue.empty():'''
		#time.sleep(5)

		start_time = time.time()
		#TLP = pkt_queue.queue[pkt_num]
		TLP = pkt_queue.get()
		end_time = time.time()
		delay  = end_time - start_time
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print('Current Time in TLP pkt {} from EP : {}\n'.format(pkt_num, current_time))
		#print('DELAY: {}s : TLP {} from EP base class : {}\n'.format(delay, pkt_num, TLP))
		print('TLP {} from EP base class : {}\n'.format(pkt_num, TLP))
		base_rec_queue.put(TLP)
		#tlp_temp = base_rec_queue.queue[pkt_num]
		#print('TLP_temp {} from EP base class : {}\n'.format(pkt_num, tlp_temp))

		#print('\n\n********************************************** base packet number {} ***********************************************'.format(pkt_num))
		#print('base header is {}'.format(TLP))

		return TLP
		