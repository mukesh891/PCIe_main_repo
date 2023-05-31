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
class pcie_callbacks:
    error.write(" pcie callback class\n")

class pcie_ep_field(pcie_callbacks):
    error.write(" pcie_ep_field class\n")


    def pcie_fmt_err_eij(self, pkt_num):
        fmt = random.choice([7])
        error.write('PKt num {}: fmt eij err is {}\n'.format(pkt_num, fmt))
        return fmt   
    
    def pcie_type_err_eij(self, pkt_num):
        type_l = random.choice([1])
        error.write('PKt num {}: TYPE eij err is {}\n'.format(pkt_num, type_l))
        return type_l
    def pcie_TC_err_eij(self):
        TC = random.choice([1])
        error.write(' TC eij err is {}\n'.format(TC))
        return TC
    def pcie_attr1_err_eij(self):
        Attr1 = random.choice([1])
        error.write(' ATTR_byte_1_bit_2 eij err is {}\n'.format(Attr1))
        return Attr1
    def pcie_TH_err_eij(self):
        TH = random.choice([1])
        error.write(' TH eij err is {}\n'.format(TH))
        return TH
    def pcie_TD_err_eij(self):
        TD = random.choice([0])
        error.write(' TD eij err is {}\n'.format(TD))
        return TD
    def pcie_EP_err_eij(self):
        error.write(" EP eij err\n")
        EP = random.choice([1]) 
        error.write(' EP eij err is {}\n'.format(EP))
        return EP
    def pcie_attr0_err_eij(self):
        attr0 = random.choice([3])
        error.write(' ATTR_byte_3_bit5_4 eij err is {}\n'.format(attr0))
        return attr0
    def pcie_AT_err_eij(self):
        AT = random.choice([1])
        error.write(' AT eij err is {}\n'.format(AT))
        return AT
    '''def pcie_length_err_eij(self):
        length = random.choice([0])
        error.write(' length eij err is {}\n'.format(length))
        return length'''
    def pcie_Completer_ID_err_eij(self):
        Completer_ID = random.choice([0])
        error.write(' Completer_ID eij err is {}\n'.format(Completer_ID))
        return Completer_ID
    '''def pcie_Compl_Status_err_eij(self):
        Compl_Status = random.choice([0,2,3,5])
        error.write(' Compl_Status eij err is {}'.format(Compl_Status))
        return Compl_Status'''
    def pcie_BCM_err_eij(self):
        error.write(" BCM eij err\n")
        BCM = random.choice([1])
        error.write(' BCM eij err is {}\n'.format(BCM))
        return BCM
    '''def pcie_Byte_Count_err_eij(self):
        Byte_Count = random.choice([0,2,3,5])
        error.write(' Byte_Count eij err is {}\n'.format(Byte_Count))
        return Byte_Count'''
    def pcie_Requester_ID_err_eij(self):
        Requester_ID = random.choice([0])
        error.write(' Requester_ID eij err is {}\n'.format(Requester_ID))
        return Requester_ID
    '''def pcie_Tag_err_eij(self):
        error.write(" Tag eij err ")
        Tag = random.choice([13])
        error.write(' Tag eij err is {}\n'.format(Tag))
        return Tag'''
    '''def pcie_Lower_Address_err_eij(self):
        error.write("  eij err ")
        Lower_Address = random.choice([0,1,2,3,5,6,7])
        error.write(' Lower_Address eij err is {}\n'.format(Lower_Address)))
        return Lower_Address'''
    
