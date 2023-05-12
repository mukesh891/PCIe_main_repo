#from pcie_ep_com_file import *
#from pcie_ep_base import *
#from pcie_com_file import compl_pkt_queue
from pcie_ep_pkt_checker import *
from pcie_ep_config_space_type0 import *
from tabulate import tabulate

completer_rec = open('completer_rec.txt', 'w')

class ep_pkt_completer(ep_base_pkt):
	def tlp_compl_fn(self, pkt_num):
		temp_valid_pkts = pkt_with_flag_queue.queue[pkt_num]
		valid_pkts = temp_valid_pkts[:-1]
		#valid_pkts = pkt_valid_queue.queue[pkt_num]
		completer_rec.write('\n priting cfg request TLP -- {} \n'.format(valid_pkts))
		base_TLP = ep_base_pkt.checker_fn_base(self, pkt_num)

		if(base_TLP == valid_pkts):		#here i am checking if the packet received from rc and ep_checker is same, because might be some fields got overwriten, in that case completion status will be 100 and fmt: 000
			header = valid_pkts[0:96]
			data = valid_pkts[96:128]
			Fmt_l = valid_pkts[0:3]
			
			if(int(Fmt_l[1], 2) == 1):
				Fmt = format(0, '03b')
				ep_cfg_space_type0.ep_config_space_fn(pkt_num, data) 
			else:
				Fmt = format(2, '03b')
				data_from_cfg = ep_cfg_space_type0.ep_config_space_fn(pkt_num, None)
				#print('data_from_cfg init {}'.format(data_from_cfg))
			
			Type = format(10, '05b')
			TC = valid_pkts[9:12]
			Attr1 = valid_pkts[13]
			TH = format(0, '01b')
			TD = valid_pkts[16]
			EP = valid_pkts[17]
			Attr0 = valid_pkts[18:20]
			AT = format(0, '02b')
			Length = valid_pkts[22:32]
			
			#Completion_Id = valid_pkts[64:80]
			Completion_Id = format(random.getrandbits(16), '016b')
			
			if(int(temp_valid_pkts[-1], 2) == 0):
				Compl_status = format(0, '03b')
			else:
				Compl_status = format(1, '03b')
			
			#Compl_status = format(0, '03b')
			BCM = format(0, '01b')
			Byte_count = format(int(Length, 2), '012b')
			Requester_Id = valid_pkts[32:48]
			Tag = valid_pkts[48:56]
			Lower_address = format(random.getrandbits(7), '07b')
			#EP = format(0, '03b')
		else:
			header = base_TLP[0:96]
			data = base_TLP[96:128]

			Fmt_l = base_TLP[0:3]

		
			Fmt = format(0, '03b')
			Type = format(10, '05b')
			TC = base_TLP[9:12]
			Attr1 = base_TLP[13]
			TH = format(0, '01b')
			TD = base_TLP[16]
			EP = base_TLP[17]
			Attr0 = base_TLP[18:20]
			AT = format(0, '02b')
			Length = base_TLP[22:32]

			#Completion_Id = base_TLP[64:80]
			Completion_Id = format(random.getrandbits(16), '016b')
			Compl_status = format(3, '03b')
			BCM = format(0, '01b')
			Byte_count = format(int(Length, 2), '012b')

			Requester_Id = base_TLP[32:48]
			Tag = base_TLP[48:56]
			Lower_address = format(random.getrandbits(7), '07b')





		#TLP = format(0, '0128b')   #default set
		'''TLP = Fmt + Type + format(0, '01b') + TC + format(0, '01b') + Attr1 + format(0, '01b') + TH + TD + EP + Attr0 + AT + Length + Completion_Id + Compl_status + BCM + Byte_count + Requester_Id + Tag + format(0, '01b') + Lower_address
		if((int(Fmt_l[1], 2) == 1) | (Compl_status == '001')):
			TLP = TLP + format(0, '032b')
		else:
			TLP = TLP + format(random.getrandbits(32 * (int(Length, 2))), '032b')'''
		
		data = [[ Fmt, Type, '', TC, '', Attr1, '', TH, TD, EP, Attr0, AT, Length, Completion_Id, Compl_status,BCM,Byte_count, Requester_Id,Tag,'',Lower_address,'']]
		headers = [ 'Fmt', 'Type', '', 'TC', '', 'Attr1', '', 'TH', 'TD', 'EP', 'Attr', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag', '', 'Lower_address', '']
		#headers = [ 'Fmt', 'Type', '', 'TC', '', 'Attr1', '', 'TH', 'TD', 'EP', 'Attr', 'AT', 'Length','Requester_Id', 'Tag','Last_DW_BE','First_DW_BE ','Completion_Id ','','Ext_Reg_no', 'Register_no',''] 
		table = tabulate(data, headers=headers, tablefmt='orgtbl')
		completer_rec.write(table)
		
		
		
		TLP = Fmt + Type + format(0, '01b') + TC + format(0, '01b') + Attr1 + format(0, '01b') + TH + TD + EP + Attr0 + AT + Length + Completion_Id + Compl_status + BCM + Byte_count + Requester_Id + Tag + format(0, '01b') + Lower_address
		data_size = '0' + str(32 * int(Length, 2)) + 'b'
		
		if((int(Fmt_l[1], 2) == 1) | (int(temp_valid_pkts[-1], 2) != 0)):  # data will be zero if either packet is invalid or config write tlp
			data = 0
			TLP = TLP + format(data, data_size)
		else:
			data = int(data_from_cfg, 2)
			print('data {}'.format(data))
			print('data_from_cfg {}'.format(data_from_cfg))
			TLP = TLP + format(data, data_size)
			

		completer_rec.write('\n priting complition TLP -- {} \n'.format(TLP))
		
		

		compl_pkt_queue.put(TLP)

		
		




