from pcie_com_file import *
from pcie_ep_base import *
import random
from tabulate import tabulate
from pcie_com_file import *
from pcie_ep_cfg_pkt import *

logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_mem_pkt.py file")
#logging.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For Generation of MEM TLP : ep_logs/ep_mem_pkt.txt")

dict_mem = {}


#mem_tx = open('ep_logs/ep_mem_pkt.txt', 'w')

class pcie_ep_mem_pkt(ep_base_pkt):
	def __init__(self):
		super.__init__(self)
		
	
	def mem_tx_fn(self, pkt_num):
		Fmt = random.choice([0, 2])	
		Type = random.choice([0])	
		T9 = 0
		TC = 0
		T8 = 0
		Attr1 = 0
		LN = 0
		TH = 0
		TD = 0
		EP = 0
		Attr0 = 0
		AT = 0
		Length = 1

		Requester_Id = 540
		Tag = 0
		
		
		if(pkt_num % 2 == 0):
			Fmt = 2
			Address = random.getrandbits(30)
			Last_DW_BE = random.getrandbits(4)
			First_DW_BE = random.getrandbits(4)
			dict_mem['Address'] = Address
			dict_mem['Last_DW_BE'] = Last_DW_BE
			dict_mem['First_DW_BE'] = First_DW_BE
		else:
			Fmt = 0
			Address = dict_mem['Address']
			Last_DW_BE = dict_mem['Last_DW_BE']
			First_DW_BE = dict_mem['First_DW_BE']
			
		Rsv_11_1 = 0

		
		


		Fmt_str = format(Fmt, '03b')
		Type_str = format(Type, '05b')
		T9_str = format(T9, '01b')
		TC_str = format(TC, '03b')
		T8_str = format(T8, '01b')
		Attr1_str = format(Attr1, '01b')
		LN_str = format(LN, '01b')
		TH_str = format(TH, '01b')
		TD_str = format(TD, '01b')
		EP_str = format(EP, '01b')
		Attr0_str = format(Attr0, '02b')
		AT_str = format(AT, '02b')
		Length_str = format(Length, '010b')

		Requester_Id_str = format(Requester_Id, '016b')
		Tag_str = format(Tag, '08b')
		Last_DW_BE_str = format(Last_DW_BE, '04b')
		First_DW_BE_str = format(First_DW_BE, '04b')

		Address_str = format(Address, '030b')
		Rsv_11_1_str = format(Rsv_11_1, '02b')
		if(Fmt_str[1] == '1'):
			Payload = random.getrandbits(32*Length)
		else:
			Payload = 0
		
		Length_size = '0' + str(32*Length) + 'b'
		Payload_str = format(Payload, Length_size)

		TLP = Fmt_str + Type_str + T9_str + TC_str + T8_str + Attr1_str + LN_str + TH_str + TD_str + EP_str + Attr0_str + AT_str + Length_str + Requester_Id_str + Tag_str + Last_DW_BE_str +First_DW_BE_str + Address_str + Rsv_11_1_str + Payload_str

		pkt_tlp_tb = [[ Fmt_str, Type_str, T9_str, TC_str, T8_str, Attr1_str, LN_str, TH_str, TD_str, EP_str, Attr0_str, AT_str, Length_str, Requester_Id_str, Tag_str, Last_DW_BE_str, First_DW_BE_str, Address_str,Rsv_11_1_str,Payload_str, '']]
		names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Address_str','Rsv_11_1','Payload_str', '']
		table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
		#mem_tx.write('MEMORY TLP {} : {}\n\n'.format(pkt_num, TLP))
		#mem_tx.write(table)
		#mem_tx.write('\n\n\n\n')

		tx_send_ep.write('MEMORY TLP {} : {}\n\n'.format(pkt_num, TLP))
		tx_send_ep.write(table)
		tx_send_ep.write('\n\n\n\n')

		#print('start of mem ep_tx {}'.format(pkt_num))
		#print('TLP {}'.format(TLP))

		return TLP