import console_to_log
from pcie_ep_base import *
from pcie_ep_com_file import *
from tabulate import tabulate
print("checker block")

received_pkt = open("received_pkt.txt","w")
received_valid_pkt = open("received_valid_pkt.txt","w")
received_invalid_pkt = open("received_invalid_pkt.txt","w")
#log_file = open("log.txt", "w")

class ep_check_pkt(ep_base_pkt):


	def ep_fn(self, pkt_num):
		TLP = ep_base_pkt.checker_fn_base(self, pkt_num)
		received_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
		received_pkt.write('header is {}, Data is {}\n'.format(hex(int(TLP[0:96], 2)), hex(int(TLP[96:128], 2))))

		'''log_file.write('\n\n********************************* TLP number {} **********************************\n'.format(pkt_num))
		log_file.write('inherited TLP is {}\n'.format(TLP))'''

		print('********************************* TLP number {} **********************************'.format(pkt_num))
		print('inherited TLP is {}\n'.format(TLP))
		Fmt = TLP[0:3]		
		Type = TLP[3:8]
		T9 = TLP[8]
		TC = TLP[9:12]
		T8 = TLP[12]
		Attr1 = TLP[13]
		LN = TLP[14]
		TH = TLP[15]
		TD = TLP[16]
		EP = TLP[17]
		Attr0 = TLP[18:20]
		AT = TLP[20:22]
		Length = TLP[22:32]

		Requester_Id = TLP[32:48]
		Tag = TLP[48:56]
		Last_DW_BE = TLP[56:60]
		First_DW_BE = TLP[60:64]

		Completion_Id = TLP[64:80]
		Rsv_10_7 = TLP[80:84]       # reserved byte 10- bit 7:4
		Ext_Register_Num = TLP[84:88]
		Register_Num = TLP[88:94]
		Rsv_11_1 = TLP[94:96]       # reserved byte 11- bit 1:0
		
		header = TLP[0:96]
		Data = TLP[96:128]


		
		'''print('ep_fn Fmt = {}\n' 'type {}\n' 'TC is {}\n' 'Attr1 is {}\n' 'Attr0 is {}\n' 'Final Attr is {}\n' 'TH is {}\n' 'TD is {}\n' 'EP is {}\n' 'AT is {}\n' 'Length is {}\n'
		'Requester ID is {}\n' 'Tag is {}\n' 'Last DW BE is {}\n' 'First DW BE is {}\n' 'Completion ID is {}\n' 'External Register Num is {}\n' 'Register Num is {}\n'
		'Data is {}\n'
		.format(Fmt, Type, TC, Attr1, Attr0, Attr, TH, TD, EP, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id, Ext_Register_Num, Register_Num, Data))'''
		
		'''log_file.write('ep_fn Fmt = {}\n' 'type {}\n' 'TC is {}\n' 'Attr1 is {}\n' 'Attr0 is {}\n' 'Final Attr is {}\n' 'TH is {}\n' 'TD is {}\n' 'EP is {}\n' 'AT is {}\n' 'Length is {}\n'
        'Requester ID is {}\n' 'Tag is {}\n' 'Last DW BE is {}\n' 'First DW BE is {}\n' 'Completion ID is {}\n' 'External Register Num is {}\n' 'Register Num is {}\n'
        'Data is {}\n'
        .format(Fmt, Type, TC, Attr1, Attr0, Attr, TH, TD, EP, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id, Ext_Register_Num, Register_Num, Data))'''

		data = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id,Rsv_10_7, Ext_Register_Num, Register_Num,Rsv_11_1,Data, '']]
		headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id','Rsv_10_7', 'Ext_Register_Num', 'Register_Num','Rsv_11_1','Data', '']
		table = tabulate(data, headers=headers, tablefmt='orgtbl')
		print(table)
		#log_file.write(table)


		
		
		Fmt_int = int(Fmt, 2)		
		Type_int = int(Type, 2)
		T9_int = int(T9, 2)
		TC_int = int(TC, 2)
		T8_int = int(T8, 2)
		Attr1_int = int(Attr1, 2)
		LN_int = int(LN, 2)
		TH_int = int(TH, 2)
		TD_int = int(TD, 2)
		EP_int = int(EP, 2)
		Attr0_int = int(Attr0, 2)
		AT_int = int(AT, 2)
		Length_int = int(Length, 2)

		'''Bus_int = int(Bus, 2)
		Device_int = int(Device, 2)
		Function_int = int(Function, 2)'''
		Requester_Id_int = int(Requester_Id, 2)
		Tag_int = int(Tag, 2)
		Last_DW_BE_int = int(Last_DW_BE, 2)
		First_DW_BE_int = int(First_DW_BE, 2)
		

		Completion_Id_int = int(Completion_Id, 2)
		Rsv_10_7_int = int(Rsv_10_7, 2)
		Ext_Register_Num_int = int(Ext_Register_Num, 2)
		Register_Num_int = int(Register_Num, 2)
		Rsv_11_1_int = int(Rsv_11_1, 2)

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
					print('INVALID TLP: Data no received for Write request')
					received_invalid_pkt.write('INVALID TLP: Data no received for Write request\n')
					if Type not in ['00000', '00010', '00100', '00101', '01100', '01101', '01110']:
						print('INVALID TLP: invalid Type for Write request: Value {}'.format(Type))
						received_invalid_pkt.write('INVALID TLP: invalid Type for Write request: Value {}\n'.format(Type))
						false_pkt += 1
				'''else:
					true_pkt += 1'''
			else:
				if(Data_int != 0):
					print('INVALID TLP: Data received for Read request')
					received_invalid_pkt.write('INVALID TLP: Data received for Read request\n')
					if Type not in ['00000', '00001', '00010', '00100', '00101']:
						print('INVALID TLP: invalid Type for Read request: Value {}'.format(Type))
						received_invalid_pkt.write('INVALID TLP: invalid Type for Read request: Value {}\n'.format(Type))
						false_pkt += 1
				'''else:
					true_pkt += 1'''



			#checking for all type possibilities
			if Type not in ['00000', '00001', '00010', '00100', '00101', '01100', '01101', '01110']:
				print('TLP is INVALID due to invalid Type: Value {}'.format(Type))
				received_invalid_pkt.write('TLP is INVALID due to invalid Type: Value {}\n'.format(Type))
				false_pkt += 1				
			'''else:
				true_pkt += 1'''


			#checking for poisoned data
			if (EP_int):
				print('TLP is INVALID due to POISONED Data: Value {}'.format(EP_int))
				received_invalid_pkt.write('TLP is INVALID due to POISONED Data: Value {}\n'.format(EP_int))
				false_pkt += 1
			'''else:
				true_pkt += 1'''



			#checking for data size w.r.to length
			if (len(Data) != (Length_int * 32)):
				print('TLP is INVALID due to invalid Data size: Data size is {} and length is {}'.format(len(Data), Length_int))
				received_invalid_pkt.write('TLP is INVALID due to invalid Data size: Data size is {} and length is {}'.format(len(Data), Length_int))
				false_pkt += 1
			'''else:
				true_pkt += 1'''
        
        
        
			#checking for configuration request type possibilities
			if (int(Type[2], 2)):   #  bit 2 of type must be 1 for cfg request
				if (TC_int==0):      # must be 0 for cfg
					if (Attr1_int==0):   # must be reserved for cfg
						if (TH_int==0):    # must be reserved for cfg
							if (Attr0_int==0):   # must be 0 for cfg
								if (AT_int==0):    # must be 0 for cfg
									if (Last_DW_BE_int==0):  # must be 0 for cfg
										if(int(Register_Num[-2:], 2) == 0):  # last two bits must be 0
											if Type in ['00100']: #since this is an endpoint so request should be for type 0
												if (Length_int == 1):   # must be 1 for cfg
													if ((32*Length_int) == len(Data)):   # data must be equal to length in DW
														if(Completion_Id_int == 0):    # completion ID must be 0 
															if(len(TLP) == (32*4)):   #TLP  size must be 4DW (including 1DW data)
																if(LN_int == 0):  # must be reserved for cfg
																	if(T9_int == 0):   # must be reserved for cfg
																		if(T8_int == 0):   # must be reserved for cfg
																			if(Rsv_10_7_int == 0):   # must be reserved for cfg
																				if(Rsv_11_1_int == 0):  # must be reserved for cfg
																					if Fmt in ['000', '010']:  # must be either 000 or 010
																						true_pkt += 1
																					else:
																						print('INVALID TLP: for CFG request, FMT must be either 000 or 010: value {}'.format(Fmt))
																						received_invalid_pkt.write('INVALID TLP: for CFG request, FMT must be either 000 or 010: value {}\n'.format(Fmt))
																						false_pkt += 1
																				else:
																					print('INVALID TLP: for CFG request, byte 11 bit 1:0 must be reserved: value {}'.format(Rsv_11_1_int)) 
																					received_invalid_pkt.write('INVALID TLP: for CFG request, byte 11 bit 1:0 must be reserved: value {}\n'.format(Rsv_11_1_int))
																					false_pkt += 1
																			else:
																				print('INVALID TLP: for CFG request, byte 10 bit 7:4 must be reserved: value {}'.format(Rsv_10_7_int)) 
																				received_invalid_pkt.write('INVALID TLP: for CFG request, byte 10 bit 7:4 must be reserved: value {}\n'.format(Rsv_10_7_int))
																				false_pkt += 1
																		else:
																			print('INVALID TLP: for CFG request, T8 must be reserved: value {}'.format(T8_int)) 
																			received_invalid_pkt.write('INVALID TLP: for CFG request, T8 must be reserved: value {}\n'.format(T8_int))
																			false_pkt += 1
																	else:
																		print('INVALID TLP: for CFG request, T9 must be reserved: value {}'.format(T9_int)) 
																		received_invalid_pkt.write('INVALID TLP: for CFG request, T9 must be reserved: value {}\n'.format(T9_int))
																		false_pkt += 1
																else:
																	print('INVALID TLP: for CFG request, LN is reserved: value {}'.format(LN_int)) 
																	received_invalid_pkt.write('INVALID TLP: for CFG request, LN is reserved: value {}\n'.format(LN_int))
																	false_pkt += 1
															else:
																print('INVALID TLP: for CFG request, LENGTH of the TLP must be 4DW (including 1DW data): TLP size {} Data size {}'.format(len(TLP), len(Data))) 
																received_invalid_pkt.write('INVALID TLP: for CFG request, LENGTH of the TLP must be 4DW (including 1DW data): TLP size {} Data size {}\n'.format(len(TLP), len(Data)))
																false_pkt += 1
														else:
															print('INVALID TLP: for CFG request, Comepltion ID must be 0: Value {}'.format(Completion_Id_int)) 
															received_invalid_pkt.write('INVALID TLP: for CFG request, Comepltion ID must be 0: Value {}\n'.format(Completion_Id_int))
															false_pkt += 1
													else:
														print('INVALID TLP: for CFG request, DATA should be 1DW: Value {} SIZE {}'.format(Data_int, len(Data))) 
														received_invalid_pkt.write('INVALID TLP: for CFG request, DATA should be 1DW: Value {} SIZE {}\n'.format(Data_int, len(Data)))
														false_pkt += 1
												else:
													print('INVALID TLP: for CFG request, Length is not 1: Value {}'.format(Length_int)) 
													received_invalid_pkt.write('INVALID TLP: for CFG request, Length is not 1: Value {}\n'.format(Length_int))
													false_pkt += 1
											else:
												print('INVALID TLP: for CFG request for EP, TYPE is not 00100: Value {}'.format(Type))
												received_invalid_pkt.write('INVALID TLP: for CFG request for EP, TYPE is not 00100: Value {}\n'.format(Type))
												false_pkt += 1
										else:
											print('INVALID TLP: for CFG request, last two bits of Register Number is not ZERO: Value {}'.format(Register_Num))
											received_invalid_pkt.write('INVALID TLP: for CFG request, last two bits of Register Number is not ZERO: Value {}\n'.format(Register_Num))
											false_pkt += 1
									else:
										print('INVALID TLP: for CFG request, last DW BE is not ZERO: Value {}'.format(Last_DW_BE_int))
										received_invalid_pkt.write('INVALID TLP: for CFG request, last DW BE is not ZERO: Value {}\n'.format(Last_DW_BE_int))
										false_pkt += 1
								else:
									print('INVALID TLP: for CFG request, AT is not ZERO: Value {}'.format(AT_int))
									received_invalid_pkt.write('INVALID TLP: for CFG request, AT is not ZERO: Value {}\n'.format(AT_int))
									false_pkt += 1
							else:
								print('INVALID TLP: for CFG request, ATTR(byte 2) is not ZERO: Value {}'.format(Attr0_int))
								received_invalid_pkt.write('INVALID TLP: for CFG request, ATTR(byte 2) is not ZERO: Value {}\n'.format(Attr0_int))
								false_pkt += 1
						else:
							print('INVALID TLP: for CFG request, TH is not ZERO: Value {}'.format(TH_int))
							received_invalid_pkt.write('INVALID TLP: for CFG request, TH is not ZERO: Value {}\n'.format(TH_int))
							false_pkt += 1
					else:
						print('INVALID TLP: for CFG request, ATTR(byte 1) is not ZERO: Value {}'.format(Attr1_int))
						received_invalid_pkt.write('INVALID TLP: for CFG request, ATTR(byte 1) is not ZERO: Value {}\n'.format(Attr1_int))
						false_pkt += 1
				else:
					print('INVALID TLP: for CFG request, TC is not ZERO: Value {}'.format(TC_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, TC is not ZERO: Value {}\n'.format(TC_int))
					false_pkt += 1
			


			




		tlp_size = '0' + str(len(TLP)) + 'b'
		tlp_flag_size = '0' + str(len(TLP) + 1) + 'b'       # size is TLP+1, 1 for flag
		v_tlp = format(0, tlp_flag_size)
		inv_tlp = format(0, tlp_flag_size)

		if(false_pkt):
			received_invalid_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
			received_invalid_pkt.write('header is {}, Data is {}\n'.format(hex(header_int), hex(Data_int)))
			received_invalid_pkt.write('{}\n'.format(table))
			inv_tlp = TLP + '1'   # adding this 1 because, 1 indicates that the error_flag is 1 (as a indication for ERROR from requested TLP)
			pkt_with_flag_queue.put(inv_tlp)  # sending TLPs(including flag) to another queue so that it will help me during completion process 
			return False
		else:
			received_valid_pkt.write('TLP: {} {}\n'.format((TLP[0:96]), (TLP[96:128])))
			received_valid_pkt.write('header is {}, Data is {}\n'.format(hex(header_int), hex(Data_int)))
			
			received_valid_pkt.write('{}\n'.format(table))
			
      		#need to modify it furthere just made it for checking purpose"
			if(pkt_num==5):
				print('pkt num is 5')
				TLP = format((int(TLP, 2) + 0), tlp_size)  # if adding 1, than tlp is overriten 
			v_tlp = TLP + '0'   # adding this 0 because, 0 indicates that the error_flag is 0 (as a indication for NO ERROR from requested TLP)
			pkt_with_flag_queue.put(v_tlp)  # sending TLPs(including flag) to another queue so that it will help me during completion process 
			return True