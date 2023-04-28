from pcie_rc_config_pkt import *
from pcie_pkt_checker import *
from pcie_com_file import *

c1 = checker_pkt()
inval_pkt = 0
val_pkt = 0
inval_pkt_num = []
val_pkt_num = []

# Open a file to store the output
filename = 'output_checker.txt'
with open(filename, 'w') as f:
	for i in range(num_packets):
		p2 = pcie_seq_rc_config_pkt()
		p2.cf0_pkt()
		p2.print_bdf()
		if not c1.checker_fn():
			print('\n ******************Packet failed the checker!***************************')
			inval_pkt += 1
			inval_pkt_num.append(i)
			f.write('\n**********************************************************************\n')
			f.write('****************Packet failed the checker!***************************\n')
			f.write('**********************************************************************\n')
		else:
			print('\n\n********************Packet passed the checker!**************************')
			val_pkt += 1
			val_pkt_num.append(i)
			f.write('\n**********************************************************************\n')
			f.write('**********************Packet passed the checker!************************\n')
			f.write('**********************************************************************\n')


		f.write('\n Generated packet {} dictionary: {}\n'.format(i, pkt_dict))
		f.write('\n Checked packet {} dictionary: {}\n'.format(i, pkt_dict))
		f.write('**********************************************************************\n')
	
	f.write("\n Number of invalid packets: {}\n".format(inval_pkt))
	f.write("Number of valid packets: {}\n".format(val_pkt))
	f.write("Invalid packet numbers: {}\n".format(inval_pkt_num))
	f.write("Valid packet numbers: {}\n".format(val_pkt_num))

# Move output file to directory

import shutil
import os

output_file = 'output_checker.txt'
destination = 'Desktop/pcie/pkt_28_4/new_file_acc_to_checker'

shutil.move(output_file, os.path.join(destination, output_file))

print(f"File '{output_file}' moved to directory: {destination}")
