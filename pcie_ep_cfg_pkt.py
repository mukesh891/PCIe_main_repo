from pcie_com_file import *
from pcie_ep_base import *
import random
from tabulate import tabulate
from pcie_com_file import *

logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_cfg_pkt.py file")
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For Generation of CFG/MEM TLP : ep_logs/ep_tx_send_pkt.txt")
#logging.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For Generation of CFG TLP : ep_logs/ep_cfg_pkt.txt")



dict_cfg = {}


#cfg_tx = open('ep_logs/ep_cfg_pkt.txt', 'w')
tx_send_ep = open('ep_logs/ep_tx_send_pkt.txt', 'w')

class pcie_ep_cfg_pkt(ep_base_pkt):
	def __init__(self):
		super.__init__(self)


	def cfg_tx_fn(self, pkt_num):
		Fmt = random.choice([0, 2])	
		Type = 5
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
		Last_DW_BE = 0
		First_DW_BE = random.getrandbits(4)

		Completion_Id = 0
		Rsv_10_7 = 0       # reserved byte 10- bit 7:4
		Ext_Register_Num = random.getrandbits(4)
		Register_Num = random.getrandbits(6)
		Rsv_11_1 = 0


		if(pkt_num % 2 == 0):
			Fmt = 2
			Ext_Register_Num = random.getrandbits(4)
			Register_Num = random.getrandbits(6)
			Last_DW_BE = random.getrandbits(4)
			First_DW_BE = random.getrandbits(4)

			dict_cfg['Ext_Register_Num'] = Ext_Register_Num
			dict_cfg['Register_Num'] = Register_Num
			dict_cfg['Last_DW_BE'] = Last_DW_BE
			dict_cfg['First_DW_BE'] = First_DW_BE
		else:
			Fmt = 0
			Ext_Register_Num = dict_cfg['Ext_Register_Num']
			Register_Num = dict_cfg['Register_Num'] 
			Last_DW_BE = dict_cfg['Last_DW_BE']
			First_DW_BE = dict_cfg['First_DW_BE']
		


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

		Completion_Id_str = format(Completion_Id, '016b')
		Rsv_10_7_str = format(Rsv_10_7, '04b')       # reserved byte 10- bit 7:4
		Ext_Register_Num_str = format(Ext_Register_Num, '04b')
		Register_Num_str = format(Register_Num, '06b')
		Rsv_11_1_str = format(Rsv_11_1, '02b')
		if(Fmt_str[1] == '1'):
			Payload = random.getrandbits(32*1)
		else:
			Payload = 0
		
		Payload_str = format(Payload, '032b')

		TLP = Fmt_str + Type_str + T9_str + TC_str + T8_str + Attr1_str + LN_str + TH_str + TD_str + EP_str + Attr0_str + AT_str + Length_str + Requester_Id_str + Tag_str + Last_DW_BE_str +First_DW_BE_str + Completion_Id_str + Rsv_10_7_str + Ext_Register_Num_str + Register_Num_str + Rsv_11_1_str + Payload_str
		
		pkt_tlp_tb = [[ Fmt_str, Type_str, T9_str, TC_str, T8_str, Attr1_str, LN_str, TH_str, TD_str, EP_str, Attr0_str, AT_str, Length_str, Requester_Id_str, Tag_str, Last_DW_BE_str, First_DW_BE_str, Completion_Id_str,Rsv_10_7_str, Ext_Register_Num_str, Register_Num_str,Rsv_11_1_str,Payload_str, '']]
		names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id','Rsv_10_7', 'Ext_Register_Num', 'Register_Num','Rsv_11_1','Payload_str', '']
		table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
		#cfg_tx.write('CFG TLP {} : {}\n\n'.format(pkt_num, TLP))
		#cfg_tx.write(table)
		#cfg_tx.write('\n\n\n\n')

		tx_send_ep.write('CFG TLP {} : {}\n\n'.format(pkt_num, TLP))
		tx_send_ep.write(table)
		tx_send_ep.write('\n\n\n\n')



		#print('start of cfg ep_tx {}'.format(pkt_num))
		#print('TLP {}'.format(TLP))

		return TLP
