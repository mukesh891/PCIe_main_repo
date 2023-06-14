import random, time
import concurrent.futures
#from pkt_dict import *
from pcie_com_file import *
from pcie_rc_base_test import *


from pcie_rc_driver import *
from pcie_ep_pkt_checker import *
#from pcie_rc_config_pkt import *
#from pcie_ep_pkt_checker import *
from pcie_ep_pkt_completer import *
from pcie_rc_rx_pkt_checker import *
#from pcie_ep_config_space_type0 import *
#from pcie_ep_memory_space import *

import console_to_log



#c1 = ep_check_pkt()

# Redirect console output to a log file
console_to_log.redirect_output_to_file()
#bin_f.close()                              #not required here as the its closing inside the generator

drv = pcie_rc_driver() 
check = pcie_rc_rx_pkt_checker()

#rc_pkts_size = pkt_queue.qrc_pkts_size()
rc_pkts_size = num_pkts
ep_pkts_size = num_ep_pkt_tx
'''arr = []
if(err_eij): 
    while len(arr) < err_pkt_no:
        num = random.randrange(0,num_pkts)
        if num not in arr:
            arr.append(num)
        arr.sort()'''
		#print()

def main_rc_to_ep(num):
    start_time = time.time()
	#if num in arr else 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cfg1_rc_to_ep = executor.submit(drv.drive_tx())
        ep1_rc_to_ep = executor.submit(call_checker_class.call_checker_fn(num))
        cpl1_rc_to_ep = executor.submit(ep_pkt_completer.pkt_compl_fn(num, ep_err_eij))
        rc_rx_check = executor.submit(check.rc_rx_checker())
		
        results = [cfg1_rc_to_ep, ep1_rc_to_ep, cpl1_rc_to_ep, rc_rx_check]
        
        for future in concurrent.futures.as_completed(results):
            if future == cfg1_rc_to_ep:
                #result1 = future.result()
            	result1_time = time.time()
            	#print("Result 1: Time:", result1_time - start_time, "seconds")
            elif future == ep1_rc_to_ep:
                #result2 = future.result()
            	result2_time = time.time()
            	#print("Result 2: Time:", result2_time - start_time, "seconds")
            elif future == cpl1_rc_to_ep:
                #result2 = future.result()
            	result3_time = time.time()
            	#print("Result 3: Time:", result3_time - start_time, "seconds")
            elif future == rc_rx_check:
                result4_time = time.time()
        
        #combined_result = result1 + result2
        
        end_time = time.time()
        
        #print("Combined Result:", combined_result)
        print("\nTotal Execution Time:", end_time - start_time, "seconds\n\n\n\n")


def main_ep_to_rc(num):
    start_time = time.time()
	#if num in arr else 0
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        ep2_ep_to_rc = executor.submit(ep_pkt_completer.ep_pkt_tx_fn(num, ep_err_eij))
        rc_rx_check = executor.submit(check.rc_rx_checker())
        results = [ep2_ep_to_rc, rc_rx_check]

        for future in concurrent.futures.as_completed(results):
            if future == ep2_ep_to_rc:
                #result1 = future.result()
                result1_time = time.time()
                #print("Result 1: Time:", result1_time - start_time, "seconds")
            elif future == rc_rx_check:
                #result2 = future.result()
                result2_time = time.time()
                #print("Result 2: Time:", result2_time - start_time, "seconds")

        #combined_result = result1 + result2

        end_time = time.time()

        #print("Combined Result:", combined_result)
        #print("Total Execution Time:", end_time - start_time, "seconds")



if __name__ == '__main__':
	start_time = time.time()
	for i in range(rc_pkts_size):
		main_rc_to_ep(i)
	start_time_ep = time.time()
	for j in range(ep_pkts_size):
		main_ep_to_rc(j)

	end_time = time.time()
	end_time_ep = time.time()
	print("\n\n\n\n\nTotal Simularion  Time:", end_time - start_time, "seconds")
	err_bin_compl2.write("\nTotal Execution Time of EP TX, Time: {} seconds\n".format(end_time_ep - start_time_ep))





err_id_f.close() 
err_bin_f.close()
bin_f.close()
from pcie_rc_tx_monitor import *





'''for i in range(rc_pkts_size):
	#c1.ep_fn(i)
	if not c1.ep_fn(i):
		print('Packet failed the end-point!\n\n\n\n')
    #print('\033[31mPacket failed the end-point!\033[0m')          #for printing in red colour
		#log_file.write('\n Packet failed the end-point!\n')
		received_pkt.write('Packet failed the end-point!\n\n')
		received_invalid_pkt.write('Packet failed the end-point!\n\n\n\n\n')
		inval_pkt += 1
		inval_pkt_num.append(i)
	else:
		print('Packet passed the end-point!\n\n\n\n')
    #print('\033[32mPacket passed the end-point!\n\033[0m')       #for printing in green colour
		#log_file.write('\n Packet passed the end-point!\n')
		received_pkt.write('Packet passed the end-point!\n\n')
		received_valid_pkt.write('Packet passed the end-point!\n\n\n\n\n')
		val_pkt_num.append(i)
		val_pkt += 1

	if i == rc_pkts_size-1:
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
		received_valid_pkt.write("valid packet numbers are {}\n".format(val_pkt_num))'''

print("number of invalid packets checked from EP {}".format(inval_pkt['index']))
print("number of valid packets checked from EP {}".format(val_pkt['index']))
print("invalid packet numbers checked from EP {}".format(inval_pkt_num))
print("valid packet numbers checked from EP {}".format(val_pkt_num))
received_pkt.close()
received_invalid_pkt.close()
received_valid_pkt.close()



#valid_pkt_size = pkt_with_flag_queue.qsize()
#comp1 = ep_pkt_completer()
#comp1 = tlp_compl_fn()



'''for i in range(valid_pkt_size):
	comp1.pkt_compl_fn(i)
for i in range(num_ep_pkt_tx):
	comp1.ep_pkt_tx_fn(i)'''
	

completer_rec.close()
binary_completer.close()


#log_file.close()

cfg.close()
mem.close()

from pcie_ep_cfg_pkt import *

from pcie_ep_mem_pkt import *
tx_send_ep.write('TOTAL TRANSMITTED TLPs {}\n\n'.format(num_ep_pkt_tx))
tx_send_ep.close()
tx_send_ep_bin.close()

err_bin_compl.close() 
err_bin_compl2.close()
error.close()

# Stop redirecting console output to the log file



#from pcie_ep_err_call_fn import *     # doing import here for err-injection to come in a flow

#check.rc_rx_checker()
#rc_checker_f.close()
#from pcie_ep_err_id import *
#from pcie_rc_memory_space import *
console_to_log.reset_output()

rc_checker_f.close()





	
