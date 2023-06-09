from email.header import Header
import console_to_log
from pcie_ep_base import *
from pcie_ep_com_file import *
from tabulate import tabulate
print("end_point block")

###### Giving info about the log files############### 
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_pkt_checker.py file")
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For knowing howmany pkt recived : ep_logs/received_pkt.txt ")
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For knowing howmany valid pkt recived : ep_logs/received_valid_pkt.txt ")
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For knowing howmany Invalid pkt recived : ep_logs/received_invalid_pkt.txt ")


received_pkt = open("ep_logs/received_pkt.txt","w")
received_valid_pkt = open("ep_logs/received_valid_pkt.txt","w")
received_invalid_pkt = open("ep_logs/received_invalid_pkt.txt","w")
#log_file = open("log.txt", "w")


inval_pkt = {'index':0}
val_pkt = {'index':0}
inval_pkt_num = [];
val_pkt_num = [];




class ep_check_pkt(ep_base_pkt):


	def ep_fn(pkt_num):
		TLP = ep_base_pkt.checker_fn_base(pkt_num)
		

		'''log_file.write('\n\n********************************* TLP number {} **********************************\n'.format(pkt_num))
		log_file.write('inherited TLP is {}\n'.format(TLP))'''

		print('********************************* TLP number {} **********************************'.format(pkt_num))
		#print('inherited TLP is {}\n'.format(TLP))
		print('TLP {} from EP checker : {}\n'.format(pkt_num, TLP))
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

		if (Type[2] == '1'):            # for cfg
			Completion_Id = TLP[64:80]
			Rsv_10_7 = TLP[80:84]       # reserved byte 10- bit 7:4
			Ext_Register_Num = TLP[84:88]
			Register_Num = TLP[88:94]
			Rsv_11_1 = TLP[94:96]       # reserved byte 11- bit 1:0
		elif(Type[:-1] == '0000'):      # for memory
			Address = TLP[64:94]
			Rsv_11_1 = TLP[94:96] 
			



		Header = TLP[0:96]
		cfg3_size = 32*3 + 32
		mem3_size = 32*3 + 32*int(Length, 2)
		mem4_size = 32*4 + 32*int(Length, 2)
		if(Type[2] == '1'):
			size_crc = cfg3_size + 32
		elif((Type[:-1] == '0000') & (Fmt[-1] == '0')):
			size_crc = mem3_size + 32
		elif((Type[:-1] == '0000') & (Fmt[-1] == '1')):
			size_crc = mem4_size + 32



		if(int(TD, 2) & (len(TLP) == size_crc)):
			Data = TLP[96:len(TLP)-32]
			TLP_wo_ecrc = TLP[:len(TLP)-32]
			ECRC = int(TLP[-32:], 2)
		else:
			Data = TLP[96:]
			TLP_wo_ecrc = TLP
			ECRC = None

		received_pkt.write('TLP: {} {} {}\n'.format(Header, Data, ECRC))
		received_pkt.write('header is {}, Data is {}, ECRC {}\n'.format( hex(int(Header, 2)), hex(int(Data, 2)), ECRC))


		if (Type[2] == '1'):            # for cfg
			pkt_tlp_tb = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id,Rsv_10_7, Ext_Register_Num, Register_Num,Rsv_11_1,Data, ECRC if int(TD, 2) else 'NONE' , '']]
			names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id','Rsv_10_7', 'Ext_Register_Num', 'Register_Num','Rsv_11_1','Data', 'ECRC', '']
			table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
			print(table)
		#log_file.write(table)
		elif(Type[:-1] == '0000'):      # for memory
			pkt_tlp_tb = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Address, Rsv_11_1,Data,  ECRC if int(TD, 2) else 'NONE' ,'']]
			names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Address','Rsv_11_1','Data', 'ECRC', '']
			table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
			print(table)

		if(TD == '1'):
			ECRC_check = int(TLP_wo_ecrc, 2) % int(fixed_ecrc_divisor, 2)			
		else:
			ECRC_check = None
			
		
		
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
		
		if (Type[2] == '1'):                      # for cfg
			Completion_Id_int = int(Completion_Id, 2)
			Rsv_10_7_int = int(Rsv_10_7, 2)
			Ext_Register_Num_int = int(Ext_Register_Num, 2)
			Register_Num_int = int(Register_Num, 2)
			Rsv_11_1_int = int(Rsv_11_1, 2)
		elif(Type[:-1] == '0000'):                # for memory
			Address_int = int(Address, 2)
			Rsv_11_1_int = int(Rsv_11_1, 2)       # reserved byte 11- bit 1:0

		


		false_pkt = 0
		true_pkt = 0

		if not (0 <= Fmt_int < 2**3 and 0 <= Type_int < 2**5 and 0 <= TC_int < 2**3 and 0 <= Attr1_int <= 1 and 0 <= TH_int <= 1 and 0 <= TD_int <= 1 and 0 <= EP_int <= 1 and 
		  0 <= Attr0_int < 2**2 and 0 <= AT_int < 2**2 and 0 <= Length_int < 2**10 and 0 <= Requester_Id_int < 2**16 and 0 <= Tag_int < 2**8 and 0 <= Last_DW_BE_int < 2**4 and 
		  0 <= First_DW_BE_int < 2**4):
			
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
			'''if(Completion_Id_int >= 2**16):
				print('INVALID Completion_Id, value: {}'.format(Completion_Id_int))
				received_invalid_pkt.write('INVALID Completion_Id, value: {}\n'.format(Completion_Id_int))
			if(Ext_Register_Num_int >= 2**4):
				print('INVALID Ext_Register_Num, value: {}'.format(Ext_Register_Num_int))
				received_invalid_pkt.write('INVALID Ext_Register_Num, value: {}\n'.format(Ext_Register_Num_int))
			if(Register_Num_int >= 2**6):
				print('INVALID Register_Num, value: {}'.format(Register_Num_int))
				received_invalid_pkt.write('INVALID Register_Num, value: {}\n'.format(Register_Num_int))
			'''		
			false_pkt += 1
		else:
			#checking for fmt write/read and its respective type possibilities			
			if(int(Fmt[1], 2)):
				if(int(Data, 2) == 0):
					print('INVALID TLP: Data not received for Write request')
					received_invalid_pkt.write('INVALID TLP: Data no received for Write request\n')
					false_pkt += 1
				if Type not in ['00000', '00010', '00100', '00101', '01100', '01101', '01110']:
					print('INVALID TLP: invalid Type for Write request: Value {}'.format(Type))
					received_invalid_pkt.write('INVALID TLP: invalid Type for Write request: Value {}\n'.format(Type))
					false_pkt += 1
				'''else:
					true_pkt += 1'''
			else:
				if(int(Data, 2) != 0):
					print('INVALID TLP: Data received for Read request')
					received_invalid_pkt.write('INVALID TLP: Data received for Read request\n')
					false_pkt += 1
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



			# ECRC check 
			if(ECRC_check != ECRC):
				print('TLP is INVALID due to ECRC Mismatch between RC and EP: RC-ECRC {} and EP-ECRC {}'.format(ECRC, ECRC_check))
				received_invalid_pkt.write('TLP is INVALID due to ECRC Mismatch between RC and EP: RC-ECRC {} and EP-ECRC {}'.format(ECRC, ECRC_check))
				false_pkt += 1
        
        

			if(Length_int > 1):
				LDB = 1 #'1' if Last_DW_BE_int else '0'
			else:
				LDB = 0
        
			print('printing length of TLP from end-point {}'.format(len(TLP)))
			#checking for configuration request type possibilities
			if (int(Type[2], 2)):   #  bit 2 of type must be 1 for cfg request
				if Fmt not in ['000', '010']:  # must be either 000 or 010																						
					print('INVALID TLP: for CFG request, FMT must be either 000 or 010: value {}'.format(Fmt))
					received_invalid_pkt.write('INVALID TLP: for CFG request, FMT must be either 000 or 010: value {}\n'.format(Fmt))
					false_pkt += 1
				if not (Type == '00100'): #since this is an endpoint so request should be for type 0
					print('INVALID TLP: for CFG request for EP, TYPE is not 00100: Value {}'.format(Type))
					received_invalid_pkt.write('INVALID TLP: for CFG request for EP, TYPE is not 00100: Value {}\n'.format(Type))
					false_pkt += 1
				if not (T9_int == 0):   # must be reserved for cfg
					print('INVALID TLP: for CFG request, T9 must be reserved: value {}'.format(T9_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, T9 must be reserved: value {}\n'.format(T9_int))
					false_pkt += 1
				if not (TC_int==0):      # must be 0 for cfg
					print('INVALID TLP: for CFG request, TC is not ZERO: Value {}'.format(TC_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, TC is not ZERO: Value {}\n'.format(TC_int))
					false_pkt += 1
				if not (T8_int == 0):   # must be reserved for cfg
					print('INVALID TLP: for CFG request, T8 must be reserved: value {}'.format(T8_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, T8 must be reserved: value {}\n'.format(T8_int))
					false_pkt += 1
				if not (Attr1_int==0):   # must be reserved for cfg
					print('INVALID TLP: for CFG request, ATTR(byte 1) is  ZERO: Value {}'.format(Attr1_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, ATTR(byte 1) is ZERO: Value {}\n'.format(Attr1_int))
					false_pkt += 1
				if not (LN_int == 0):  # must be reserved for cfg																														
					print('INVALID TLP: for CFG request, LN must be reserved: value {}'.format(LN_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, LN must be  reserved: value {}\n'.format(LN_int))
					false_pkt += 1
				if not (TH_int==0):    # must be reserved for cfg
					print('INVALID TLP: for CFG request, TH is not ZERO: Value {}'.format(TH_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, TH is not ZERO: Value {}\n'.format(TH_int))
					false_pkt += 1
				if not (((TD_int==1) & (ECRC != None)) | ((TD_int==0) & (ECRC == None))):    # must be reserved for cfg
					print('INVALID TLP: for CFG request, ECRC is not as per TD: TD {}, ECRC {}'.format(TD_int, ECRC))
					received_invalid_pkt.write('INVALID TLP: for CFG request, ECRC is not as per TD: TD {}, ECRC {}\n'.format(TD_int, ECRC))
					false_pkt += 1
				if not (EP_int==0):    # will be 0
					print('INVALID TLP: for CFG request, EP is not ZERO: Value {}'.format(EP_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, EP is not ZERO: Value {}\n'.format(EP_int))
					false_pkt += 1
				if not (Attr0_int==0):   # must be 0 for cfg
					print('INVALID TLP: for CFG request, ATTR(byte 2) is not ZERO: Value {}'.format(Attr0_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, ATTR(byte 2) is not ZERO: Value {}\n'.format(Attr0_int))
					false_pkt += 1
				if not (AT_int==0):    # must be 0 for cfg
					print('INVALID TLP: for CFG request, AT is not ZERO: Value {}'.format(AT_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, AT is not ZERO: Value {}\n'.format(AT_int))
					false_pkt += 1
				if not (Length_int == 1):   # must be 1 for cfg
					print('INVALID TLP: for CFG request, Length is not 1: Value {}'.format(Length_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, Length is not 1: Value {}\n'.format(Length_int))
					false_pkt += 1
				'''if not (0 <= Requester_Id_int < 2**16):    # completion ID must be 0 
					print('INVALID TLP: for CFG request, Requester ID must be 0: Value {}'.format(Requester_Id_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, Requester ID must be 0: Value {}\n'.format(Requester_Id_int))
					false_pkt += 1'''
				if not (0 <= Type_int < 2**8):    # completion ID must be 0 
					print('INVALID TLP: for CFG request, Type must be from 0 to 2**8: Value {}'.format(Type_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, Type must be from 0 to 2**8: Value {}\n'.format(Type_int))
					false_pkt += 1
				if not (Last_DW_BE_int == 0):  # must be 0 for cfg
					print('INVALID TLP: for CFG request, last DW BE is not ZERO: Value {}'.format(Last_DW_BE_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, last DW BE is not ZERO: Value {}\n'.format(Last_DW_BE_int))
					false_pkt += 1
				if not (First_DW_BE_int != 0):  # must be 0 for cfg
					print('INVALID TLP: for CFG request, First_DW_BE is not 0011: Value {}'.format(First_DW_BE))
					received_invalid_pkt.write('INVALID TLP: for CFG request, First_DW_BE is not 0011: Value {}\n'.format(First_DW_BE))
					false_pkt += 1
				if not (Completion_Id_int == 0):    # completion ID must be 0 
					print('INVALID TLP: for CFG request, Comepltion ID must be 0: Value {}'.format(Completion_Id_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, Comepltion ID must be 0: Value {}\n'.format(Completion_Id_int))
					false_pkt += 1
				if not (Rsv_10_7_int == 0):   # must be reserved for cfg
					print('INVALID TLP: for CFG request, byte 10 bit 7:4 must be reserved: value {}'.format(Rsv_10_7_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, byte 10 bit 7:4 must be reserved: value {}\n'.format(Rsv_10_7_int))
					false_pkt += 1
				'''if not (0 <= Ext_Register_Num_int < 2**4):  # last two bits must be 0
					print('INVALID TLP: for CFG request, Ext_Register_Num_int must be between 0 and 2**4: Value {}'.format(Ext_Register_Num_int))
					received_invalid_pkt.write('INVALID TLP: for CFG request, last two bits of Register Number is not ZERO: Value {}\n'.format(Ext_Register_Num_int))
					false_pkt += 1'''
				if not (int(Register_Num[-2:], 2) == 0):  # last two bits must be 0
					print('INVALID TLP: for CFG request, last two bits of Register Number is not ZERO: Value {}'.format(Register_Num))
					received_invalid_pkt.write('INVALID TLP: for CFG request, last two bits of Register Number is not ZERO: Value {}\n'.format(Register_Num))
					false_pkt += 1		
				if not (Rsv_11_1_int == 0):  # must be reserved for cfg																											
					print('INVALID TLP: for CFG request, byte 11 bit 1:0 must be reserved: value {}'.format(Rsv_11_1_int)) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, byte 11 bit 1:0 must be reserved: value {}\n'.format(Rsv_11_1_int))
					false_pkt += 1
				if not ((32*Length_int) == len(Data)):   # data must be equal to length in DW:
					print('INVALID TLP: for CFG request, DATA should be 1DW: Length in bits {} SIZE of Data{}'.format(32*Length_int, len(Data))) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, DATA should be 1DW: Length in bits {} SIZE of Data{}\n'.format(32*Length_int, len(Data)))
					false_pkt += 1			
				if not (len(TLP) == (32*3) + 32 + (32 if TD_int else 0)):   #TLP  size must be 4DW (including 1DW data)
					print('INVALID TLP: for CFG request, LENGTH of the TLP must be 4DW (including 1DW data): TLP size {}'.format(len(TLP))) 
					received_invalid_pkt.write('INVALID TLP: for CFG request, LENGTH of the TLP must be 4DW (including 1DW data): TLP size {}\n'.format(len(TLP)))
					false_pkt += 1
				
				
				
				
				
				

			

			#check for memory request
			if (Type[:-1] == '0000'):   #  bit 2 of type must be 1 for Memory request
				if Fmt not in ['000', '010', '001', '011']:  # FMT must be either 000/010/001/011																						
					print('INVALID TLP: for Memory request, FMT must be either 000/010/001/011: value {}'.format(Fmt))
					received_invalid_pkt.write('INVALID TLP: for Memory request, FMT must be either 000/010/001/011: value {}\n'.format(Fmt))
					false_pkt += 1
				if Type not in ['00000', '00001']: # must be either 00000 or 00001
					print('INVALID TLP: for Memory request for EP, TYPE must be either 00000 or 00001: Value {}'.format(Type))
					received_invalid_pkt.write('INVALID TLP: for Memory request for EP, TYPE must be either 00000 or 00001: Value {}\n'.format(Type))
					false_pkt += 1
				if not (T9_int == 0):   # must be reserved for Memory
					print('INVALID TLP: for Memory request, T9 must be reserved: value {}'.format(T9_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, T9 must be reserved: value {}\n'.format(T9_int))
					false_pkt += 1
				if not (TC_int == 0):      # must be 0 because no VC defined in Cfg compatibility space
					print('INVALID TLP: for Memory request, TC must ZERO because no VC defined in Cfg compatibility space: Value {}'.format(TC_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, TC must ZERO because no VC defined in Cfg compatibility space: Value {}\n'.format(TC_int))
					false_pkt += 1
				if not (T8_int == 0):   # must be reserved for Memory
					print('INVALID TLP: for Memory request, T8 must be reserved: value {}'.format(T8_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, T8 must be reserved: value {}\n'.format(T8_int))
					false_pkt += 1
				if not (Attr1_int == 0):   # must be 0 for non- IDO
					print('INVALID TLP: for Memory request, ATTR(byte 1) must be ZERO: Value {}'.format(Attr1_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, ATTR(byte 1) must be ZERO: Value {}\n'.format(Attr1_int))
					false_pkt += 1
				if not (LN_int == 0):  # must be reserved for Memory																														
					print('INVALID TLP: for Memory request, LN is reserved: value {}'.format(LN_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, LN is reserved: value {}\n'.format(LN_int))
					false_pkt += 1
				if not (TH_int == 0):    # will be 0
					print('INVALID TLP: for Memory request, TH is not ZERO: Value {}'.format(TH_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, TH is not ZERO: Value {}\n'.format(TH_int))
					false_pkt += 1
				if not (((TD_int==1) & (ECRC != None)) | ((TD_int==0) & (ECRC == None))):    # 
					print('INVALID TLP: for Memory request, ECRC is not as per TD: TD {}, ECRC {}'.format(TD_int, ECRC))
					received_invalid_pkt.write('INVALID TLP: for Memory request, ECRC is not as per TD: TD {}, ECRC {}\n'.format(TD_int, ECRC))
					false_pkt += 1
				if not (EP_int == 0):    # will be 0
					print('INVALID TLP: for Memory request, EP is not ZERO: Value {}'.format(EP_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, EP is not ZERO: Value {}\n'.format(EP_int))
					false_pkt += 1
				if not (Attr0_int == 0):   # will be 0 because there is no snoop and relaxed odering is not set 
					print('INVALID TLP: for Memory request, ATTR(byte 2) is not ZERO: Value {}'.format(Attr0_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, ATTR(byte 2) is not ZERO: Value {}\n'.format(Attr0_int))
					false_pkt += 1
				if not (AT_int == 0):    # will be 0 since no address translation done
					print('INVALID TLP: for Memory request, AT is not ZERO: Value {}'.format(AT_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, AT is not ZERO: Value {}\n'.format(AT_int))
					false_pkt += 1
				if not (0 <= Length_int < 2**10):   # Length must be between 0 - 2**10
					print('INVALID TLP: for Memory request, Length must be between 0 - 2**10: Value {}'.format(Length_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, Length must be between 0 - 2**10: Value {}\n'.format(Length_int))
					false_pkt += 1
				if not (0 <= Requester_Id_int < 2**16):    # Requester must be between 0 - 2**16 
					print('INVALID TLP: for Memory request, Requester must be between 0 - 2**16: Value {}'.format(Requester_Id_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, Requester must be between 0 - 2**16: Value {}\n'.format(Requester_Id_int))
					false_pkt += 1
				if not (0 <= Type_int < 2**8):    # Type must be from 0 to 2**8
					print('INVALID TLP: for Memory request, Type must be from 0 to 2**8: Value {}'.format(Type_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, Type must be from 0 to 2**8: Value {}\n'.format(Type_int))
					false_pkt += 1
				if not (((Last_DW_BE_int!=0) & (LDB!=0)) | ((Last_DW_BE_int==0) & (LDB==0))):  # must be as per length
					print('INVALID TLP: for Memory request, last DW BE not as per length: Value {}'.format(Last_DW_BE_int))
					received_invalid_pkt.write('INVALID TLP: for Memory request, last DW BE not as per length: Value {}\n'.format(Last_DW_BE_int))
					false_pkt += 1
				if not (First_DW_BE_int != 0):  # First_DW_BE must be non-zero
					print('INVALID TLP: for Memory request, First_DW_BE is not as per length: Value {}'.format(First_DW_BE))
					received_invalid_pkt.write('INVALID TLP: for Memory request, First_DW_BE is not as per length: Value {}\n'.format(First_DW_BE))
					false_pkt += 1
				if not (0 <= Address_int < 2**30):    # Address_int must be non-zero 
					print('INVALID TLP: for Memory request, Address must be between 0 to 2**30: Value {}'.format(Address_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, Address must be between 0 to 2**30: Value {}\n'.format(Address_int))
					false_pkt += 1
				if not (Rsv_11_1_int == 0):  # must be reserved for Memory																											
					print('INVALID TLP: for Memory request, byte 11 bit 1:0 must be reserved: value {}'.format(Rsv_11_1_int)) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, byte 11 bit 1:0 must be reserved: value {}\n'.format(Rsv_11_1_int))
					false_pkt += 1
				if not ((32*Length_int) == len(Data)):   # data size must be equal to length in bits:
					print('INVALID TLP: for Memory request, DATA is not matching with Lenght: Length in bits {} SIZE of Data{}'.format(32*Length_int, len(Data))) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, DATA should be 1DW: Length in bits {} SIZE of Data{}'.format(32*Length_int, len(Data)))
					false_pkt += 1			
				if not (len(TLP) == (32*3) + (32*Length_int) + (32 if int(Fmt[-1], 2) else 0) + (32 if TD_int else 0)):   #TLP  size must be 4DW (including 1DW data) + 1DW (if header is 4 DW )
					print('INVALID TLP: for Memory request, LENGTH of TLP must be 4DW (including 1DW data) + 1DW (if header is 4 DW ): Length of TLP {}'.format(len(TLP))) 
					received_invalid_pkt.write('INVALID TLP: for Memory request, LENGTH of the TLP must be 4DW (including 1DW data) + 1DW (if header is 4 DW ): Length of TLP {}'.format(len(TLP)))
					false_pkt += 1


			

			# following big endian rule
			fdata0 = Data[-8:] if int(First_DW_BE[-1], 2) else format(0, '08b')
			fdata1 = Data[-16:-8] if int(First_DW_BE[-2], 2) else format(0, '08b')
			fdata2 = Data[-24:-16] if int(First_DW_BE[-3], 2) else format(0, '08b')
			fdata3 = Data[-32:-24] if int(First_DW_BE[-4], 2) else format(0, '08b')
			#Data = fdata3 + fdata2 + fdata1 + fdata0

			ldata3 = Data[:8] if int(Last_DW_BE[-4], 2) else format(0, '08b')
			ldata2 = Data[8:16] if int(Last_DW_BE[-3], 2) else format(0, '08b')
			ldata1 = Data[16:24] if int(Last_DW_BE[-2], 2) else format(0, '08b')
			ldata0 = Data[24:32] if int(Last_DW_BE[-1], 2) else format(0, '08b')


			if(Length_int == 1):
				Data = fdata3 + fdata2 + fdata1 + fdata0
			elif(Length_int == 2):
				Data = ldata3 + ldata2 + ldata1 + ldata0 + fdata3 + fdata2 + fdata1 + fdata0
			else:
				Data = ldata3 + ldata2 + ldata1 + ldata0 + Data[-((32*Length_int)-32):-32] + fdata3 + fdata2 + fdata1 + fdata0
			

		#TLP = 0
		if(int(TD, 2) & (len(TLP) == size_crc)):
			TLP = Header + Data + format(ECRC, '032b')
		else:
			TLP = Header + Data 

		Header_int = int(Header, 2)
		Data_int = int(Data, 2)

		tlp_size = '0' + str(len(TLP)) + 'b'
		tlp_flag_size = '0' + str(len(TLP) + 1) + 'b'       # size is TLP+1, 1 for flag
		v_tlp = format(0, tlp_flag_size)
		inv_tlp = format(0, tlp_flag_size)

		if(false_pkt):
			received_invalid_pkt.write('TLP: {} {} {}\n'.format(Header, Data, ECRC))
			received_invalid_pkt.write('header is {}, Data is {}, ECRC {}\n'.format( hex(int(Header, 2)), hex(int(Data, 2)), ECRC))
			received_invalid_pkt.write('{}\n'.format(table))

			print('\n*** EP_CHECKER_ERR_ID_{} ***'.format(pkt_num))
			inval_pkt_num.append(pkt_num)
			inval_pkt['index'] = inval_pkt['index'] + 1

			print('Packet failed the end-point!')
			#print('\033[31mPacket failed the end-point!\033[0m')          #for printing in red colour
			#log_file.write('\n Packet failed the end-point!\n')
			received_pkt.write('Packet failed the end-point!\n\n')
			received_invalid_pkt.write('Packet failed the end-point!\n\n\n\n\n')

			inv_tlp = TLP + '1'   # adding this 1 because, 1 indicates that the error_flag is 1 (as a indication for ERROR from requested TLP)
			pkt_with_flag_queue.put(inv_tlp)  # sending TLPs(including flag) to another queue so that it will help me during completion process 
			return False
		else:
			received_valid_pkt.write('TLP: {} {} {}\n'.format(Header, Data, ECRC))
			received_valid_pkt.write('header is {}, Data is {}, ECRC {}\n'.format( hex(int(Header, 2)), hex(int(Data, 2)), ECRC))		
			received_valid_pkt.write('{}\n'.format(table))

			val_pkt_num.append(pkt_num)
			val_pkt['index'] = val_pkt['index'] + 1
			print('Packet passed the end-point!')
			 #print('\033[32mPacket passed the end-point!\n\033[0m')       #for printing in green colour
			#log_file.write('\n Packet passed the end-point!\n')
			received_pkt.write('Packet passed the end-point!\n\n')
			received_valid_pkt.write('Packet passed the end-point!\n\n\n\n\n')

      		#need to modify it furthere just made it for checking purpose"
			if(pkt_num==5):
				#print('pkt num is 5')
				TLP = format((int(TLP, 2) + 0), tlp_size)  # if adding 1, than tlp is overriten 
			v_tlp = TLP + '0'   # adding this 0 because, 0 indicates that the error_flag is 0 (as a indication for NO ERROR from requested TLP)
			pkt_with_flag_queue.put(v_tlp)  # sending TLPs(including flag) to another queue so that it will help me during completion process 
			return True

class call_checker_class():
	def call_checker_fn(pkt_num):
		ep_check_pkt.ep_fn(pkt_num)
