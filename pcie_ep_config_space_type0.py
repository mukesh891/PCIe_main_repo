import random
#from pkt_dict import *
from pcie_com_file import *
from pcie_ep_com_file import *
from array import array

print("ep_cfg_space_type0 block")

cfg_array = array('Q', [0] * 16)   # Q = unsigned 8 bytes storage in each index


#default set for configuration header type 0
type0header_size = '0' + str(16*32) + 'b'
type_0_header = format(0, type0header_size)


#DW0
Vendor_ID = format(540, '016b')						  # offset 00 hwinit
Device_ID = format(2, '016b')						  # offset 02 hwinit
#DW1
Command = format(0b100, '016b')						  # offset 04 
Status = format(0b10000, '016b')		    		  # offset 06
#DW2
Rev_ID = format(1, '08b')						      # offset 08 hwinit
Class_Code = format(0, '024b')					      # offset 09 r-only
#DW3
Cache_line_Size = format(64, '08b')                   # offset 0c software
Latency_Timer = format(0, '08b')					  # offset 0d 

Header_Type = format(0b10000000, '08b')				  # offset 0e 
BIST = format(0, '08b')		             			  # offset 0f 
#DW4
BAR0 = format(0xffffffff, '032b')					  # offset 10 
#DW5
BAR1 = format(0xffffffff, '032b')					  # offset 14 
#DW6
BAR2 = format(0xffffffff, '032b')					  # offset 18 
#DW7
BAR3 = format(0xffffffff, '032b')				      # offset 1c 
#DW8
BAR4 = format(0xffffffff, '032b')				      # offset 20 
#DW9
BAR5 = format(0xffffffff, '032b')				      # offset 24 
#DW10
CardBus_CIS_Pointer = format(1, '032b')               # offset 28 
#DW11
Subsystem_Vendor_ID = format(540, '016b')             # offset 2c 
Subsystem_Device_ID = format(2, '016b')               # offset 2e 
#DW12
Expansion_ROM_Base_Address = format(0xa0f00,'032b')   # offset 30 - last bit is for E-ROM disabled if 0
#DW13 
Capability_Pointer = format(0b10101100, '08b')        # offset 34- last two bits must be 0
Reserved0 = format(0, '024b')                         # offset 35 
#DW14
Reserved1 = format(1, '032b')                         # offset 38 
#DW15
Interrupt_Line = format(0, '08b')                     # offset 3c 
Interrupt_Pin = format(0, '08b')                      # offset 3d 
Min_Gnt = format(0, '08b')                            # offset 3e 
Max_Lat = format(1, '08b')                            # offset 3f 

BAR0 = format((int(BAR0, 2) & 0xFFFFC000), '032b')
BAR1 = format((int(BAR1, 2) & 0xFFFFFC00), '032b')
BAR2 = format((int(BAR2, 2) & 0xFFFFC000), '032b')
BAR3 = format((int(BAR3, 2) & 0xFFFFFC00), '032b')
BAR4 = format((int(BAR4, 2) & 0xFFFFC000), '032b')
BAR5 = format((int(BAR5, 2) & 0xFFFFFC00), '032b')
type_0_header = Max_Lat + Min_Gnt + Interrupt_Pin + Interrupt_Line + Reserved1 + Reserved0 + Capability_Pointer + Expansion_ROM_Base_Address + Subsystem_Device_ID + Subsystem_Vendor_ID + CardBus_CIS_Pointer + BAR5 + BAR4 + BAR3 + BAR2 + BAR1 + BAR0 + BIST + Header_Type + Latency_Timer + Cache_line_Size + Class_Code + Rev_ID + Status + Command + Device_ID + Vendor_ID
		

for i in range(16):
	if(i==0):
		cfg_array[i%16] = int(type_0_header[-32:], 2)
	else:
		cfg_array[i%16] = int(type_0_header[-(32*(i+1)):-(32*(i))], 2)






cfg = open('cfg_values.txt', 'w')
class ep_cfg_space_type0():		
	def ep_config_space_fn(pkt_num, data_rec):
		#print('ep_config_space header is {}'.format(TLP))
		temp_valid_pkts = pkt_with_flag_queue.queue[pkt_num]
		valid_pkts = temp_valid_pkts[:-1]
		error_flag = temp_valid_pkts[-1]


		'''
		if(error_flag):
			compl_st = '0000'
		else:
			compl_st = '0001'
		Bist = '1' + '0' + '00' + compl_st
 
		BIST = format(int(Bist, 2), '08b')					  # offset 0f 
		
		
		BAR0 = format((random.getrandbits(32) & 0xFFFFC000), '032b')
		BAR1 = format((random.getrandbits(32) & 0xFFFFFC00), '032b')
		BAR2 = format((random.getrandbits(32) & 0xFFFFC000), '032b')
		BAR3 = format((random.getrandbits(32) & 0xFFFFFC00), '032b')
		BAR4 = format((random.getrandbits(32) & 0xFFFFC000), '032b')
		BAR5 = format((random.getrandbits(32) & 0xFFFFFC00), '032b')
		type_0_header = Max_Lat + Min_Gnt + Interrupt_Pin + Interrupt_Line + Reserved1 + Reserved0 + Capability_Pointer + Expansion_ROM_Base_Address + Subsystem_Device_ID + Subsystem_Vendor_ID + CardBus_CIS_Pointer + BAR5 + BAR4 + BAR3 + BAR2 + BAR1 + BAR0 + BIST + Header_Type + Latency_Timer + Cache_line_Size + Class_Code + Rev_ID + Status + Command + Device_ID + Vendor_ID
		'''



		data_sent = 0
		if (error_flag == '0'):
			index = pkt_num % 16
			if(valid_pkts[1] == '0'):
				#write_count += 1				
				data_sent = format(cfg_array[index], '032b')				
			else:
				data_sent = 0

				if(index == 4):
					data_rec = int(data_rec, 2) & 0xFFFFC000
				elif(index == 5):
					data_rec = int(data_rec, 2) & 0xFFFFFC00
				elif(index == 6):
					data_rec = int(data_rec, 2) & 0xFFFFC000
				elif(index == 7):
					data_rec = int(data_rec, 2) & 0xFFFFFC00
				elif(index == 8):
					data_rec = int(data_rec, 2) & 0xFFFFC000
				elif(index == 9):
					data_rec = int(data_rec, 2) & 0xFFFFFC00
				else:
					data_rec = int(data_rec, 2)

				cfg_array[index] = data_rec		
		else:
			data_sent = 0


		type_0_header = format(cfg_array[15], '032b') + format(cfg_array[14], '032b') + format(cfg_array[13], '032b') + format(cfg_array[12], '032b') + format(cfg_array[11], '032b') + \
			format(cfg_array[10], '032b') + format(cfg_array[9], '032b') + format(cfg_array[8], '032b') + format(cfg_array[7], '032b') + format(cfg_array[6], '032b') + \
			format(cfg_array[5], '032b') + format(cfg_array[4], '032b') + format(cfg_array[3], '032b') + format(cfg_array[2], '032b') + format(cfg_array[1], '032b') + \
			format(cfg_array[0], '032b')

		#print('printing type 0 header value from base\n' '{}'.format(type_0_header))
		cfg.write('printing type 0 header value from base\n' '{}\n'.format(type_0_header))
		#print('printing data value from base\n' '{}'.format(data_sent))

		return data_sent

		
		