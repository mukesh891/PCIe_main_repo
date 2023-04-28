from pcie_rc_config_pkt import *
from pcie_pkt_checker import *
from pcie_com_file import *


c1 = checker_pkt()
inval_pkt = 0
val_pkt = 0
inval_pkt_num = [];
val_pkt_num = [];

for i in range(num_packets):
	p2 = pcie_seq_rc_config_pkt()
	p2.cf0_pkt()
	p2.print_bdf()
	if not c1.checker_fn():
		print('Packet failed the checker!')
		inval_pkt += 1
		inval_pkt_num.append(i)
	else:
		print('Packet passed the checker!')
		val_pkt_num.append(i)
		val_pkt += 1

	if i == num_packets-1:
		print("number of invalid packets are {}".format(inval_pkt))
		print("number of valid packets are {}".format(val_pkt))
		print("invalid packet numbers are {}".format(inval_pkt_num))
		print("valid packet numbers are {}".format(val_pkt_num))