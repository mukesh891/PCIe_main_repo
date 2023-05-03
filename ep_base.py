import random
#from pkt_dict import *
from pcie_com_file import *


print("ep_base_pkt block")



class ep_base_pkt():
	
	
	def checker_fn_base(self, pkt_num):
		
		TLP = format(0, '0128b')   #default set
		TLP = pkt_queue.queue[pkt_num]

		print('********************************************** base packet number {} ***********************************************'.format(pkt_num))
		print('base header is {}'.format(TLP))

		return TLP
		