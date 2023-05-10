
#from pkt_dict import *
from pcie_com_file import *
from pcie_rc_config_pkt import *
from pcie_ep_pkt_checker import *
from pcie_ep_pkt_completer import *
#from pcie_rc_checker_pkt import *
import console_to_log
c1 = ep_check_pkt()
inval_pkt = 0
val_pkt = 0
inval_pkt_num = [];
val_pkt_num = [];
# Redirect console output to a log file
console_to_log.redirect_output_to_file()
#bin_f.close()                              #not required here as the its closing inside the generator


size = pkt_queue.qsize()
for i in range(size):
	if not c1.ep_fn(i):
		print('\n Packet failed the checker!\n')
    #print('\033[31mPacket failed the checker!\033[0m')          #for printing in red colour
		#log_file.write('\n Packet failed the checker!\n')
		received_pkt.write('Packet failed the checker!\n\n')
		received_invalid_pkt.write('Packet failed the checker!\n\n\n\n\n')
		inval_pkt += 1
		inval_pkt_num.append(i)
	else:
		print('\n Packet passed the checker!\n')
    #print('\033[32mPacket passed the checker!\n\033[0m')       #for printing in green colour
		#log_file.write('\n Packet passed the checker!\n')
		received_pkt.write('Packet passed the checker!\n\n')
		received_valid_pkt.write('Packet passed the checker!\n\n\n\n\n')
		val_pkt_num.append(i)
		val_pkt += 1

	if i == size-1:
		print("number of invalid packets are {}".format(inval_pkt))
		print("number of valid packets are {}".format(val_pkt))
		print("invalid packet numbers are {}".format(inval_pkt_num))
		print("valid packet numbers are {}".format(val_pkt_num))

		#log_file.write("number of invalid packets are {}\n".format(inval_pkt))
		#log_file.write("number of valid packets are {}\n".format(val_pkt))
		#log_file.write("invalid packet numbers are {}\n".format(inval_pkt_num))
		#log_file.write("valid packet numbers are {}\n".format(val_pkt_num))

		received_pkt.write("number of invalid packets are {}\n".format(inval_pkt))
		received_pkt.write("invalid packet numbers are {}\n".format(inval_pkt_num))
		received_invalid_pkt.write("number of invalid packets are {}\n".format(inval_pkt))
		received_invalid_pkt.write("invalid packet numbers are {}\n".format(inval_pkt_num))

		received_pkt.write("number of valid packets are {}\n".format(val_pkt))
		received_pkt.write("valid packet numbers are {}\n".format(val_pkt_num))
		received_valid_pkt.write("number of valid packets are {}\n".format(val_pkt))
		received_valid_pkt.write("valid packet numbers are {}\n".format(val_pkt_num))


received_pkt.close()
received_invalid_pkt.close()
received_valid_pkt.close()



valid_pkt_size = pkt_with_flag_queue.qsize()
comp1 = ep_pkt_completer()
#rc_check = pcie_rc_checker_pkt()

for i in range(valid_pkt_size):
	comp1.tlp_compl_fn(i)

completer_rec.close()

'''send_compl_pkt_size = compl_pkt_queue.qsize()
for i in range(send_compl_pkt_size):
	rc_check.rc_checker_fn(i)
comp_send.close()'''

#log_file.close()
# Stop redirecting console output to the log file
console_to_log.reset_output()






	
