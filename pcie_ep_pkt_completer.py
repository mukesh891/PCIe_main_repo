#from pcie_ep_com_file import *
#from pcie_ep_base import *
#from pcie_com_file import compl_pkt_queue
from pcie_ep_pkt_checker import *
from pcie_ep_config_space_type0 import *
from pcie_ep_memory_space import *
from tabulate import tabulate

completer_rec = open('completer_rec.txt', 'w')

class ep_pkt_completer(ep_base_pkt):
	def pkt_compl_fn(self, pkt_num):
		temp_valid_pkts = pkt_with_flag_queue.queue[pkt_num]   # getting the request TLP from queue (stored by ep_checker)
		valid_pkts = temp_valid_pkts[:-1]                      #since last bit is for flat, not including the last bit
		
		
		#print('packet {} \n' '{}'.format(pkt_num, valid_pkts))
		#completer_rec.write('priting packet {} from completer\n' '{}\n'.format(pkt_num, valid_pkts))
		#completer_rec.write('priting packet including flag {} from completer\n' '{}\n'.format(pkt_num, temp_valid_pkts))
		completer_rec.write('\n priting cfg request TLP {} -- {} \n'.format(pkt_num, valid_pkts))

		base_TLP = ep_base_pkt.checker_fn_base(self, pkt_num)   # getting the request TLP directly from base

		if((int(base_TLP[:96], 2) == int(valid_pkts[:96], 2))):		#here i am checking if the packet received from rc and ep_checker is same, because might be some fields got overriten, in that case completion status will be 100 and fmt: 000
			completer_rec.write('\n Error not injected in checker \n')
			header = valid_pkts[0:96]
			data = valid_pkts[96:128]

			Fmt_l = valid_pkts[0:3]
			Type_l = valid_pkts[3:8]
			length_l = valid_pkts[22:32]
			Address_l = valid_pkts[64:94]
			'''if(temp_valid_pkts[-1] == '0'):
				Address_l = valid_pkts[64:126] if int(Fmt_l[-1], 2) else valid_pkts[64:94]
			else:
				if(len(valid_pkts) == 32*3):
					Address_l = valid_pkts[64:94]
				else:
					Address_l = valid_pkts[64:126]'''
			

		
			if(int(Fmt_l[1], 2) == 1):
				Fmt = format(0, '03b')				
			else:
				Fmt = format(2, '03b')				

			Type = format(10, '05b')
			T9 = format(0, '01b')
			TC = valid_pkts[9:12]                # must be same as request
			T8 = format(0, '01b')
			Attr1 = valid_pkts[13]               # must be same as request
			LN = format(0, '01b')                # LN is clear since request is not LN read/write
			TH = format(0, '01b')
			TD = valid_pkts[16]
			EP = valid_pkts[17]
			Attr0 = valid_pkts[18:20]            # must be same as request
			AT = format(0, '02b')                # must be 0 for receivers
			Length = valid_pkts[22:32]

			Completion_Id = format(522, '016b')
			if(int(temp_valid_pkts[-1], 2) == 0):
				Compl_status = format(0, '03b')  # status 0 if completer succesfully sends the TLP with no error 
			else:
				Compl_status = format(1, '03b')  # status 1 if completer identifies a error in the requested TLP 
			BCM = format(0, '01b')               # only be set by PCI-x, so for PCIe its always 0
			Byte_count = format(4, '012b')       # excluding memory read compl & atomic compl, byte count must be 4

			Requester_Id = valid_pkts[32:48]     # must be same as request
			Tag = valid_pkts[48:56]              # must be same as request
			Rsv_11_7 = format(0, '01b')          # byte 11 bit 7 is reserved
			Lower_address = format(0, '07b')     # excluding memory read compl & atomic compl, byte count must be 0
		
			completer_rec.write('enabling type check\n')
			if(Type_l[2] == '1'):
				completer_rec.write('entered type check for cfg\n')
				if(Fmt_l == '010'):
					completer_rec.write('entered fmt check for cfg\n')
					ep_cfg_space_type0.ep_config_space_fn(pkt_num, data, Compl_status)                    # if request is write/cmpl w/o data than send the data as an argument
					completer_rec.write('cfg write done')
				elif(Fmt_l == '000'):
					completer_data = ep_cfg_space_type0.ep_config_space_fn(pkt_num, None, Compl_status)    # if request is read/cmpl w/ data than get the data from cfg space
					completer_rec.write('cfg read done')
			elif(Type_l[:-1] == '0000'):
				completer_rec.write('entered type check for memory\n')
				if(Fmt_l == '010'):
					completer_rec.write('entered fmt check for memory\n')
					pcie_ep_memory_space.write_request(pkt_num, int(Address_l, 2), int(data, 2))                    # if request is write/cmpl w/o data than send the data as an argument
					completer_rec.write('memory write done\n')
				elif(Fmt_l == '000'):
					completer_data = pcie_ep_memory_space.read_request(pkt_num, int(Address_l, 2))
					completer_rec.write('memory read done\n')
					
					

		else:
			completer_rec.write('\n Error injected in checker \n')
			header = base_TLP[0:96]
			data = base_TLP[96:128]

			Fmt_l = base_TLP[0:3]
			#Type_l = base_TLP[3:8]

		
			Fmt = format(0, '03b')
			
			Type = format(10, '05b')
			T9 = format(0, '01b')
			TC = base_TLP[9:12]                  # must be same as request
			T8 = format(0, '01b')
			Attr1 = base_TLP[13]                 # must be same as request
			LN = format(0, '01b')                # LN is clear since request is not LN read/write
			TH = format(0, '01b')
			TD = base_TLP[16]
			EP = base_TLP[17]
			Attr0 = base_TLP[18:20]              # must be same as request
			AT = format(0, '02b')                # must be 0 for receivers
			Length = base_TLP[22:32]

			Completion_Id = format(522, '016b')
			Compl_status = format(0b100, '03b')      # status 3 if some occured in completer
			BCM = format(0, '01b')               # only be set by PCI-x, so for PCIe its always 0
			Byte_count = format(4, '012b')       # excluding memory read compl & atomic compl, byte count must be 4

			Requester_Id = base_TLP[32:48]       # must be same as request
			Tag = base_TLP[48:56]                # must be same as request
			Rsv_11_7 = format(0, '01b')          # byte 11 bit 7 is reserved
			Lower_address = format(0, '07b')     # excluding memory read compl & atomic compl, byte count must be 0

			completer_data = ep_cfg_space_type0.ep_config_space_fn(pkt_num, None, Compl_status)    # sending cmpl status
			completer_data = format(0, '032b')                                                     # make the data 0
		




		#TLP = format(0, '0128b')   #default set
		TLP = Fmt + Type + T9 + TC + T8 + Attr1 + LN + TH + TD + EP + Attr0 + AT + Length + Completion_Id + Compl_status + BCM + Byte_count + Requester_Id + Tag + Rsv_11_7 + Lower_address
		data_size = '0' + str(32 * int(Length, 2)) + 'b'      # data size must always be equal to length in DW


		if((int(Fmt_l[1], 2) == 1) | (int(temp_valid_pkts[-1], 2) != 0)):  # data will be zero if either packet is invalid or config write tlp
			data = 0
			TLP = TLP + format(data, data_size)
		else:                                                     # else data is sent 
			data = int(completer_data, 2)
			TLP = TLP + format(data, data_size)
		
		data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Completion_Id, Compl_status,BCM,Byte_count, Requester_Id,Tag,Rsv_11_7,Lower_address,'']]
		headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', '']
		
		table = tabulate(data, headers=headers, tablefmt='orgtbl')
		completer_rec.write(table)
		completer_rec.write('\n priting complition TLP {} -- {} \n\n\n'.format(pkt_num, TLP))
		
		
		if not ((Type == '00000') & (Fmt == '010')):
			compl_pkt_queue.put(TLP)

		
		



