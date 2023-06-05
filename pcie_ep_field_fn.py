#from pcie_rc_config_pkt import * 
#from try_pcie_rc_cfg_base_seq import * 
import random 
from pprint import pprint
from pcie_com_file import *
#from pcie_ep_err_id import *

###### Giving info about the log files###############
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_field_fn.py file")
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For knowing The error injected IDs : ep_logs/error_inj.txt")



'''lines = open("ep_logs/binary_completer.txt","r")
line_count = 0
for i in lines:
            line_count = line_count + 1
lines.close()'''

error = open("ep_logs/error_inj.txt","w")
#class pcie_callbacks:
    #error.write(" pcie callback class\n")

class pcie_ep_field():
    #error.write(" pcie_ep_field class\n")


    def pcie_fmt_err_eij(self, pkt_num):
        fmt = random.choice([7])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} *** : fmt eij err is {}\n'.format(pkt_num, fmt))
        return fmt   
    
    def pcie_type_err_eij(self, pkt_num):
        type_l = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***: TYPE eij err is {}\n'.format(pkt_num, type_l))
        return type_l
    def pcie_TC_err_eij(self, pkt_num):
        TC = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  TC eij err is {}\n'.format(pkt_num, TC))
        return TC
    def pcie_attr1_err_eij(self, pkt_num):
        Attr1 = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  ATTR_byte_1_bit_2 eij err is {}\n'.format(pkt_num, Attr1))
        return Attr1
    def pcie_TH_err_eij(self, pkt_num):
        TH = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  TH eij err is {}\n'.format(pkt_num, TH))
        return TH
    def pcie_TD_err_eij(self, pkt_num):
        TD = random.choice([0])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  TD eij err is {}\n'.format(pkt_num, TD))
        return TD
    def pcie_EP_err_eij(self, pkt_num):
        error.write(" EP eij err\n")
        EP = random.choice([1]) 
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  EP eij err is {}\n'.format(pkt_num, EP))
        return EP
    def pcie_attr0_err_eij(self, pkt_num):
        attr0 = random.choice([3])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  ATTR_byte_3_bit5_4 eij err is {}\n'.format(pkt_num, attr0))
        return attr0
    def pcie_AT_err_eij(self, pkt_num):
        AT = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  AT eij err is {}\n'.format(pkt_num, AT))
        return AT
    '''def pcie_length_err_eij(self, pkt_num):
        length = random.choice([0])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  length eij err is {}\n'.format(pkt_num, length))
        return length'''
    def pcie_Completer_ID_err_eij(self, pkt_num):
        Completer_ID = random.choice([0])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Completer_ID eij err is {}\n'.format(pkt_num, Completer_ID))
        return Completer_ID
    '''def pcie_Compl_Status_err_eij(self, pkt_num):
        Compl_Status = random.choice([0,2,3,5])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Compl_Status eij err is {}'.format(pkt_num, Compl_Status))
        return Compl_Status'''
    def pcie_BCM_err_eij(self, pkt_num):
        BCM = random.choice([1])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  BCM eij err is {}\n'.format(pkt_num, BCM))
        return BCM
    '''def pcie_Byte_Count_err_eij(self, pkt_num):
        Byte_Count = random.choice([0,2,3,5])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Byte_Count eij err is {}\n'.format(pkt_num, Byte_Count))
        return Byte_Count'''
    def pcie_Requester_ID_err_eij(self, pkt_num):
        Requester_ID = random.choice([0])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Requester_ID eij err is {}\n'.format(pkt_num, Requester_ID))
        return Requester_ID
    '''def pcie_Tag_err_eij(self):
        Tag = random.choice([13])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Tag eij err is {}\n'.format(pkt_num, Tag))
        return Tag'''
    '''def pcie_Lower_Address_err_eij(self):
        Lower_Address = random.choice([0,1,2,3,5,6,7])
        error.write('*** EP_TRANSMITTER_ERR_ID_{} ***:  Lower_Address eij err is {}\n'.format(Lower_Address)))
        return Lower_Address'''
    
