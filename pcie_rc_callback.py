from pcie_rc_config_pkt import * 
#from try_pcie_rc_cfg_base_seq import * 

from pprint import pprint
class pcie_callbacks:
    print("This is pcie callback class")

class pcie_err_eij(pcie_callbacks):
    print("This is pcie_err_eij class")
    #def pcie_requester_id_err_eij(self):
    #   print("This is bdf eij err callback ")
    #   #pkt.cfg0_pkt()
    #   tl_pkt=pcie_rc_config_pkt()
    #   tl_pkt.requester_id=0xBADBDF
    #   print(tl_pkt.requester_id)
    #   return tl_pkt.requester_id

    def pcie_fmt_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.fmt = random.choice([1,3,4,5,6,7])
        print(tl_pkt.fmt)
        return tl_pkt.fmt   
    
    def pcie_type_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.type = random.choice([5,6,7,12,13,14,15])
        print(tl_pkt.type)
        return tl_pkt.type
    def pcie_TC_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.TC = random.choice([2,3,5])
        print(tl_pkt.TC)
        return tl_pkt.TC
    def pcie_attr1_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Attr1 = random.choice([1])
        print(tl_pkt.Attr1)
        return tl_pkt.Attr1
    def pcie_TH_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.TH = random.choice([1])
        print(tl_pkt.TH)
        return tl_pkt.TH
    def pcie_TD_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.TD = random.choice([0])
        print(tl_pkt.TD)
        return tl_pkt.TD
    def pcie_EP_err_eij(self):
        print("This is bdf eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.EP = random.choice([1,3,5]) 
        print(tl_pkt.EP)
        return tl_pkt.EP
    def pcie_attr0_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.attr0 = random.choice([1,3])
        print(tl_pkt.attr0)
        return tl_pkt.attr0
    def pcie_AT_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.AT = random.choice([2,5])
        print(tl_pkt.AT)
        return tl_pkt.AT
    def pcie_length_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.length = random.choice([0,2,4,6,8,9])
        print(tl_pkt.length)
        return tl_pkt.length
    def pcie_Tag_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Tag = random.choice([0,2,3,5])
        print(tl_pkt.Tag)
        return tl_pkt.Tag
    def pcie_Last_DW_BE_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Last_DW_BE = random.choice([0,2,3,5,7,10,13])
        print(tl_pkt.Last_DE_BE)
        return tl_pkt.Last_DW_BE
    def pcie_First_DW_BE_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.First_DW_BE = random.choice([0,1,2,3,5,6,7])
        print(tl_pkt.First_DW_BE)
        return tl_pkt.First_DW_BE
    def pcie_Completion_ID_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Completion_ID = random.choice([0,1,2,3,5,6,7])
        print(tl_pkt.Completion_ID)
        return tl_pkt.Completion_ID
    def pcie_Ext_Register_Num_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Ext_Register_Num = random.choice([0,1,2,3,5,6,7])
        print(tl_pkt.Ext_Register_Num)
        return tl_pkt.Ext_Register_Num
    def pcie_Register_Num_err_eij(self):
        print("This is  eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_config_pkt()
        tl_pkt.Register_Num = random.choice([0,1,2,3,5,6,7])
        print(tl_pkt.Register_Num)
        return tl_pkt.Register_Num  
