from ep_base import *


print("checker block")

class ep_check_pkt(ep_base_pkt):


	def ep_fn(self, pkt_num):
		header = ep_base_pkt.checker_fn_base(self, pkt_num)
		
		print('********************************* packet number {} **********************************'.format(pkt_num))
		print('inherited header is {}\n'.format(header))
		Fmt = header[0:3]		
		Type = header[3:8]
		TC = header[9:12]
		Attr1 = header[13]
		TH = header[15]
		TD = header[16]
		EP = header[17]
		Attr0 = header[18:20]
		AT = header[20:22]
		Length = header[22:32]
		Attr = Attr1 + Attr0

		'''Bus = header[32:40]
		Device = header[40:45]
		Function = header[45:48]
		Requester_Id = Bus + Device + Function'''
		Requester_Id = header[32:48]
		Tag = header[48:56]
		Last_DW_BE = header[56:60]
		First_DW_BE = header[60:64]


		Completion_Id = header[64:80]
		Ext_Register_Num = header[84:88]
		Register_Num = header[88:94]
		
		#Address = header[64:95]
		Data = header[96:128]

		
		print('ep_fn Fmt = {}\n' 'type {}\n' 'TC is {}\n' 'Attr1 is {}\n' 'Attr0 is {}\n' 'Final Attr is {}\n' 'TH is {}\n' 'TD is {}\n' 'EP is {}\n' 'AT is {}\n' 'Length is {}\n'
		'Requester ID is {}\n' 'Tag is {}\n' 'Last DW BE is {}\n' 'First DW BE is {}\n' 'Completion ID is {}\n' 'External Register Num is {}\n' 'Register Num is {}\n'
		'Data is {}\n'
		.format(Fmt, Type, TC, Attr1, Attr0, Attr, TH, TD, EP, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id, Ext_Register_Num, Register_Num, Data))

		
		
		Fmt_int = int(Fmt, 2)		
		Type_int = int(Type, 2)
		TC_int = int(TC, 2)
		Attr1_int = int(Attr1, 2)
		TH_int = int(TH, 2)
		TD_int = int(TD, 2)
		EP_int = int(EP, 2)
		Attr0_int = int(Attr0, 2)
		AT_int = int(AT, 2)
		Length_int = int(Length, 2)
		Attr_int = int(Attr, 2)

		'''Bus_int = int(Bus, 2)
		Device_int = int(Device, 2)
		Function_int = int(Function, 2)'''
		Requester_Id_int = int(Requester_Id, 2)
		Tag_int = int(Tag, 2)
		Last_DW_BE_int = int(Last_DW_BE, 2)
		First_DW_BE_int = int(First_DW_BE, 2)
		

		Completion_Id_int = int(Completion_Id, 2)
		Ext_Register_Num_int = int(Ext_Register_Num, 2)
		Register_Num_int = int(Register_Num, 2)
		Data_int = int(Data, 2)

		print('data {}'.format(Data_int))
		
		

		false_pkt = 0
		true_pkt = 0

		if not (0 <= Fmt_int < 2**3 and 0 <= Type_int < 2**5 and 0 <= TC_int < 2**3 and 0 <= Attr1_int <= 1 and 0 <= TH_int <= 1 and 0 <= TD_int <= 1 and 0 <= EP_int <= 1 and 
		  0 <= Attr0_int < 2**2 and 0 <= AT_int < 2**2 and 0 <= Length_int < 2**10 and 0 <= Requester_Id_int < 2**16 and 0 <= Tag_int < 2**8 and 0 <= Last_DW_BE_int < 2**4 and 
		  0 <= First_DW_BE_int < 2**4 and 0 <= Completion_Id_int < 2**16 and 0 <= Ext_Register_Num_int < 2**4 and 0 <= Register_Num_int < 2**6):
			
			if(Fmt_int >= 2**3):
				print('INVALID FMT, value: {}'.format(Fmt_int))
			if(Type_int >= 2**5):
				print('INVALID Type, value: {}'.format(Type_int))
			if(TC_int >= 2**3):
				print('INVALID TC, value: {}'.format(TC_int))
			if(Attr1_int!=0 | Attr1_int!=1):
				print('INVALID Attr1, value: {}'.format(Attr1_int))
			if(TH_int!=0 | TH_int!=1):
				print('INVALID TH, value: {}'.format(TH_int))
			if(TD_int!=0 | TD_int!=1):
				print('INVALID TD, value: {}'.format(TD_int))
			if(EP_int!=0 | EP_int!=1):
				print('INVALID EP, value: {}'.format(EP_int))
			if(Attr0_int >= 2**2):
				print('INVALID Attr0, value: {}'.format(Attr0_int))
			if(AT_int >= 2**2):
				print('INVALID AT, value: {}'.format(AT_int))
			if(Length_int >= 2**10):
				print('INVALID Length, value: {}'.format(Length_int))
			if(Requester_Id_int >= 2**16):
				print('INVALID Requester_Id, value: {}'.format(Requester_Id_int))
			if(Tag_int >= 2**8):
				print('INVALID Tag, value: {}'.format(Tag_int))
			if(Last_DW_BE_int >= 2**4):
				print('INVALID Last_DW_BE, value: {}'.format(Last_DW_BE_int))		
			if(First_DW_BE_int >= 2**4):
				print('INVALID First_DW_BE, value: {}'.format(First_DW_BE_int))
			if(Completion_Id_int >= 2**16):
				print('INVALID Completion_Id, value: {}'.format(Completion_Id_int))
			if(Ext_Register_Num_int >= 2**4):
				print('INVALID Ext_Register_Num, value: {}'.format(Ext_Register_Num_int))
			if(Register_Num_int >= 2**6):
				print('INVALID Register_Num, value: {}'.format(Register_Num_int))
					
			false_pkt += 1
		else:
			#checking for fmt write/read and its respective type possibilities			
			if(int(Fmt[1], 2)):
				if(Data_int == 0):
					print('Packet is INVALID due to NO DATA RECEIVED from write fmt')
					if Type not in ['00000', '00010', '00100', '00101', '01010', '01011', '01100', '01101', '01110']:
						print('Packet is INVALID due to invalid Type for write Fmt: Value {}'.format(Type))
					false_pkt += 1
				else:
					true_pkt += 1
			else:
				if(Data_int != 0):
					print('Packet is INVALID due to DATA RECEIVED from read fmt')
					if Type not in ['00000', '00001', '00010', '00100', '00101', '01010', '01011']:
						print('Packet is INVALID due to invalid Type for read Fmt: Value {}'.format(Type))
					false_pkt += 1
				else:
					true_pkt += 1



			#checking for all type possibilities
			if Type in ['00000', '00001', '00010', '00100', '00101', '01010', '01011', '01100', '01101', '01110']:
				true_pkt += 1
			else:
				print('Packet is INVALID due to invalid Type: Value {}'.format(Type))
				false_pkt += 1





		if(false_pkt):
			return False
		else:
			print("Packet is valid")
			return True

