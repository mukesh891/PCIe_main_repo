from ep_base import *


print("checker block")

received_pkt = open("received_pkt.txt","w")
received_valid_pkt = open("received_valid_pkt.txt","w")
received_invalid_pkt = open("received_invalid_pkt.txt","w")

class ep_check_pkt(ep_base_pkt):


	def ep_fn(self, pkt_num):
		TLP = ep_base_pkt.checker_fn_base(self, pkt_num)
		received_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
		received_pkt.write('header is {}, Data is {}\n'.format(hex(int(TLP[0:96], 2)), hex(int(TLP[96:128], 2))))

		print('********************************* TLP number {} **********************************'.format(pkt_num))
		print('inherited TLP is {}\n'.format(TLP))
		Fmt = TLP[0:3]		
		Type = TLP[3:8]
		TC = TLP[9:12]
		Attr1 = TLP[13]
		TH = TLP[15]
		TD = TLP[16]
		EP = TLP[17]
		Attr0 = TLP[18:20]
		AT = TLP[20:22]
		Length = TLP[22:32]
		Attr = Attr1 + Attr0

		'''Bus = TLP[32:40]
		Device = TLP[40:45]
		Function = TLP[45:48]
		Requester_Id = Bus + Device + Function'''
		Requester_Id = TLP[32:48]
		Tag = TLP[48:56]
		Last_DW_BE = TLP[56:60]
		First_DW_BE = TLP[60:64]


		Completion_Id = TLP[64:80]
		Ext_Register_Num = TLP[84:88]
		Register_Num = TLP[88:94]
		
		header = TLP[0:96]
		Data = TLP[96:128]

		
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

		header_int = int(header, 2)
		Data_int = int(Data, 2)


		false_pkt = 0
		true_pkt = 0

		if not (0 <= Fmt_int < 2**3 and 0 <= Type_int < 2**5 and 0 <= TC_int < 2**3 and 0 <= Attr1_int <= 1 and 0 <= TH_int <= 1 and 0 <= TD_int <= 1 and 0 <= EP_int <= 1 and 
		  0 <= Attr0_int < 2**2 and 0 <= AT_int < 2**2 and 0 <= Length_int < 2**10 and 0 <= Requester_Id_int < 2**16 and 0 <= Tag_int < 2**8 and 0 <= Last_DW_BE_int < 2**4 and 
		  0 <= First_DW_BE_int < 2**4 and 0 <= Completion_Id_int < 2**16 and 0 <= Ext_Register_Num_int < 2**4 and 0 <= Register_Num_int < 2**6):
			
			print('TLP is INVALID due to:')
			received_invalid_pkt.write('TLP is INVALID due to:\n')
			if(Fmt_int >= 2**3):
				print('INVALID FMT, value: {}'.format(Fmt_int))
				received_invalid_pkt.write('INVALID FMT, value: {}\n'.format(Fmt_int))
			if(Type_int >= 2**5):
				print('INVALID Type, value: {}'.format(Type_int))
				received_invalid_pkt.write('INVALID Type, value: {}\n'.format(Type_int))
			if(TC_int >= 2**3):
				print('INVALID TC, value: {}'.format(TC_int))
				received_invalid_pkt.write('INVALID TC, value: {}\n'.format(TC_int))
			if(Attr1_int!=0 | Attr1_int!=1):
				print('INVALID Attr1, value: {}'.format(Attr1_int))
				received_invalid_pkt.write('INVALID Attr1, value: {}\n'.format(Attr1_int))
			if(TH_int!=0 | TH_int!=1):
				print('INVALID TH, value: {}'.format(TH_int))
				received_invalid_pkt.write('INVALID TH, value: {}\n'.format(TH_int))
			if(TD_int!=0 | TD_int!=1):
				print('INVALID TD, value: {}'.format(TD_int))
				received_invalid_pkt.write('INVALID TD, value: {}\n'.format(TD_int))
			if(EP_int!=0 | EP_int!=1):
				print('INVALID EP, value: {}'.format(EP_int))
				received_invalid_pkt.write('INVALID EP, value: {}\n'.format(EP_int))
			if(Attr0_int >= 2**2):
				print('INVALID Attr0, value: {}'.format(Attr0_int))
				received_invalid_pkt.write('INVALID Attr0, value: {}\n'.format(Attr0_int))
			if(AT_int >= 2**2):
				print('INVALID AT, value: {}'.format(AT_int))
				received_invalid_pkt.write('INVALID AT, value: {}\n'.format(AT_int))
			if(Length_int >= 2**10):
				print('INVALID Length, value: {}'.format(Length_int))
				received_invalid_pkt.write('INVALID Length, value: {}\n'.format(Length_int))
			if(Requester_Id_int >= 2**16):
				print('INVALID Requester_Id, value: {}'.format(Requester_Id_int))
				received_invalid_pkt.write('INVALID Requester_Id, value: {}\n'.format(Requester_Id_int))
			if(Tag_int >= 2**8):
				print('INVALID Tag, value: {}'.format(Tag_int))
				received_invalid_pkt.write('INVALID Tag, value: {}\n'.format(Tag_int))
			if(Last_DW_BE_int >= 2**4):
				print('INVALID Last_DW_BE, value: {}'.format(Last_DW_BE_int))
				received_invalid_pkt.write('INVALID Last_DW_BE, value: {}\n'.format(Last_DW_BE_int))
			if(First_DW_BE_int >= 2**4):
				print('INVALID First_DW_BE, value: {}'.format(First_DW_BE_int))
				received_invalid_pkt.write('INVALID First_DW_BE, value: {}\n'.format(First_DW_BE_int))
			if(Completion_Id_int >= 2**16):
				print('INVALID Completion_Id, value: {}'.format(Completion_Id_int))
				received_invalid_pkt.write('INVALID Completion_Id, value: {}\n'.format(Completion_Id_int))
			if(Ext_Register_Num_int >= 2**4):
				print('INVALID Ext_Register_Num, value: {}'.format(Ext_Register_Num_int))
				received_invalid_pkt.write('INVALID Ext_Register_Num, value: {}\n'.format(Ext_Register_Num_int))
			if(Register_Num_int >= 2**6):
				print('INVALID Register_Num, value: {}'.format(Register_Num_int))
				received_invalid_pkt.write('INVALID Register_Num, value: {}\n'.format(Register_Num_int))
					
			false_pkt += 1
		else:
			#checking for fmt write/read and its respective type possibilities			
			if(int(Fmt[1], 2)):
				if(Data_int == 0):
					print('TLP is INVALID due to NO DATA RECEIVED from write fmt')
					received_invalid_pkt.write('TLP is INVALID due to NO DATA RECEIVED from write fmt\n')
					if Type not in ['00000', '00010', '00100', '00101', '01010', '01011', '01100', '01101', '01110']:
						print('TLP is INVALID due to invalid Type for write Fmt: Value {}'.format(Type))
						received_invalid_pkt.write('TLP is INVALID due to invalid Type for write Fmt: Value {}\n'.format(Type))
					false_pkt += 1
				else:
					true_pkt += 1
			else:
				if(Data_int != 0):
					print('TLP is INVALID due to DATA RECEIVED from read fmt')
					received_invalid_pkt.write('TLP is INVALID due to DATA RECEIVED from read fmt\n')
					if Type not in ['00000', '00001', '00010', '00100', '00101', '01010', '01011']:
						print('TLP is INVALID due to invalid Type for read Fmt: Value {}'.format(Type))
						received_invalid_pkt.write('TLP is INVALID due to invalid Type for read Fmt: Value {}\n'.format(Type))
					false_pkt += 1
				else:
					true_pkt += 1



			#checking for all type possibilities
			if Type in ['00000', '00001', '00010', '00100', '00101', '01010', '01011', '01100', '01101', '01110']:
				true_pkt += 1
			else:
				print('TLP is INVALID due to invalid Type: Value {}'.format(Type))
				received_invalid_pkt.write('TLP is INVALID due to invalid Type: Value {}\n'.format(Type))
				false_pkt += 1


			#checking for poisoned data
			if (EP_int):
				print('TLP is INVALID due to POISONED Data: Value {}'.format(EP_int))
				received_invalid_pkt.write('TLP is INVALID due to POISONED Data: Value {}\n'.format(EP_int))
				false_pkt += 1
			else:
				true_pkt += 1






		if(false_pkt):
			received_invalid_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
			received_invalid_pkt.write('header is {}, Data is {}\n'.format(hex(header_int), hex(Data_int)))
			received_invalid_pkt.write('ep_fn Fmt = {}\n' 'type {}\n' 'TC is {}\n' 'Attr1 is {}\n' 'Attr0 is {}\n' 'Final Attr is {}\n' 'TH is {}\n' 'TD is {}\n' 'EP is {}\n'
							  'AT is {}\n' 'Length is {}\n'	'Requester ID is {}\n' 'Tag is {}\n' 'Last DW BE is {}\n' 'First DW BE is {}\n' 'Completion ID is {}\n' 
							  'External Register Num is {}\n' 'Register Num is {}\n' 'Data is {}\n'.format(Fmt, Type, TC, Attr1, Attr0, Attr, TH, TD, EP, AT, Length, 
																					  Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id, Ext_Register_Num, 
																					  Register_Num, Data))
			return False
		else:
			received_valid_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
			received_valid_pkt.write('header is {}, Data is {}\n'.format(hex(header_int), hex(Data_int)))
			received_valid_pkt.write('ep_fn Fmt = {}\n' 'type {}\n' 'TC is {}\n' 'Attr1 is {}\n' 'Attr0 is {}\n' 'Final Attr is {}\n' 'TH is {}\n' 'TD is {}\n' 'EP is {}\n'
							  'AT is {}\n' 'Length is {}\n'	'Requester ID is {}\n' 'Tag is {}\n' 'Last DW BE is {}\n' 'First DW BE is {}\n' 'Completion ID is {}\n' 
							  'External Register Num is {}\n' 'Register Num is {}\n' 'Data is {}\n'.format(Fmt, Type, TC, Attr1, Attr0, Attr, TH, TD, EP, AT, Length, 
																					  Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id, Ext_Register_Num, 
																					  Register_Num, Data))
			return True

