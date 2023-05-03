from pcie_pkt_checker import *
#from pkt_dict import *
from pcie_com_file import *
from pcie_rc_config_pkt import *


c1 = ep_check_pkt()
inval_pkt = 0
val_pkt = 0
inval_pkt_num = [];
val_pkt_num = [];

p1 = pcie_seq_rc_config_pkt()
p1.cf0_pkt()


size = pkt_queue.qsize()
for i in range(size):
	if not c1.ep_fn(i):
		print('Packet failed the checker!')
		inval_pkt += 1
		inval_pkt_num.append(i)
	else:
		print('Packet passed the checker!')
		val_pkt_num.append(i)
		val_pkt += 1

	if i == size-1:
		print("\n\nnumber of invalid packets are {}".format(inval_pkt))
		print("number of valid packets are {}".format(val_pkt))
		print("invalid packet numbers are {}".format(inval_pkt_num))
		print("valid packet numbers are {}".format(val_pkt_num))
	
