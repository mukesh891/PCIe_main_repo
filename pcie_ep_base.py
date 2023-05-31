import random
import console_to_log
#from pkt_dict import *
from pcie_com_file import *

# Redirect console output to a log file
console_to_log.redirect_output_to_file()
print("ep_base_pkt block")
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_base.py file")


class ep_base_pkt():
	
	
	def checker_fn_base(self, pkt_num):
		
		TLP = format(0, '0128b')   #default set
		TLP = pkt_queue.queue[pkt_num]

		#print('\n\n********************************************** base packet number {} ***********************************************'.format(pkt_num))
		#print('base header is {}'.format(TLP))

		return TLP
		