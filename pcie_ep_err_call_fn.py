#import sys
#sys.path.append('/home/shanmukh/shanmukh_cell/1_PCIe/checker_temp')
#from pcie_com_file import *
#from pcie_ep_com_file import *
from pcie_ep_err_id import *
#from ep_logs import binary_completer
from pcie_ep_field_fn import *

good_compl = open("ep_logs/binary_completer.txt","r") 
err_bin_compl = open("ep_logs/err_binary_completer.txt","w")
'''for line1 in good_compl:
            
            line1 = line1.strip('\n')        
            err_bin_compl.write('priting pkt before bin compl {}\n'.format(line1)) ###############'''

class pcie_ep_err_call:
    def __init__(self):
        self.k=0
        self.err_id=0
    def ep_err_call_fn(self):
        
        #num_pkts= argv.num_pkts
        TLP_error = ""
        
        for line in good_compl:
            
            line = line.strip('\n')        
            #err_bin_compl.write('priting pkt from bin compl {}\n'.format(line)) ###############

            compl_qsize = pkt_valid_queue.qsize()
            #err_bin_compl.write('priting num okts from queue {}\n'.format(compl_qsize)) ###############


            if(ep_err_eij):                
                if(self.err_id < compl_qsize):                  
                    ep_err_inj_hdl = pcie_ep_field()
                    if self.err_id in ep_err_arr:          
                        #err_bin_compl.write('priting error id {}\n'.format(self.err_id))
                        j = random.choice([0,1])                      
                        if(j==0):
                
                            fmt = ep_err_inj_hdl.pcie_fmt_err_eij(self.err_id)
                            
                            fmt_str = format(fmt, '03b')       
                            #print("modified fmt->",fmt_str) 
                            TLP_error =fmt_str+line[3:]
                            compl_pkt_queue.put(TLP_error)
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            
                        # If j==0 , then "type" will be injected with error
                        if(j==1):
                            typ =ep_err_inj_hdl.pcie_type_err_eij(self.err_id)
                            type_str=format(typ, '05b')       
                            #print(type_str) 
                            TLP_error = line[:3] + type_str + line[8:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==3):
                            TC =ep_err_inj_hdl.pcie_TC_err_eij()
                            TC_str=format(TC, '03b')       
                            #print(TC_str) 
                            TLP_error = line[:9] + TC_str + line[12:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==4):
                            Attr1 =ep_err_inj_hdl.pcie_attr1_err_eij()
                            Attr1_str=format(Attr1, '01b')       
                            #print(Attr1_str) 
                            TLP_error = line[:13]+Attr1_str+line[14:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==5):
                            TH =ep_err_inj_hdl.pcie_TH_err_eij()
                            TH_str=format(TH, '01b')       
                            #print(TH_str)
                            #TLP_error = TH_str+line[:15]
                            TLP_error = line[:15]+TH_str+line[16:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==6):
                            TD =ep_err_inj_hdl.pcie_TD_err_eij()
                            TD_str=format(TD, '01b')       
                            #print(TH_str)
                            #TLP_error = TH_str+line[:15]
                            TLP_error = line[:16]+TD_str+line[17:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==7):
                            EP =ep_err_inj_hdl.pcie_EP_err_eij()
                            EP_str=format(EP, '01b')       
                            #print(EP_str) 
                            TLP_error = line[:17]+EP_str+line[18:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==8):
                            attr0 =ep_err_inj_hdl.pcie_attr0_err_eij()
                            attr0_str=format(attr0, '02b')       
                            #print(attr0_str) 
                            TLP_error = line[:18]+attr0_str+line[20:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==9):
                            AT =ep_err_inj_hdl.pcie_AT_err_eij()
                            AT_str=format(AT, '02b')       
                            #print(AT_str) 
                            TLP_error = line[:20]+AT_str+line[22:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        '''if(j==10):
                            length =ep_err_inj_hdl.pcie_length_err_eij()
                            length_str=format(length, '10b')       
                            #print(length_str) 
                            TLP_error = line[:22]+length_str+line[32:] 
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)'''
                        if(j==11):
                            Completer_ID =ep_err_inj_hdl.pcie_Completer_ID_err_eij()
                            Completer_ID_str=format(Completer_ID, '016b')
                            #print(Tag_str)
                            #TLP_error = TH_str+line[:15]
                            TLP_error = line[:32]+Completer_ID_str+line[48:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==11):
                            Compl_Status =ep_err_inj_hdl.pcie_Compl_Status_err_eij()
                            Compl_Status_str=format(Compl_Status, '03b')
                            #print(Tag_str)
                            #TLP_error = TH_str+line[:15]
                            TLP_error = line[:48]+Compl_Status_str+line[51:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        if(j==12):
                            BCM =ep_err_inj_hdl.pcie_BCM_err_eij()
                            BCM_str=format(BCM, '01b')
                            #print(Last_DW_BE_str)
                            #TLP_error = TH_str+line[:15]
                            TLP_error = line[:51]+BCM_str+line[52:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        '''if(j==13):
                            Byte_Count =ep_err_inj_hdl.pcie_Byte_Count_err_eij()
                            Byte_Count_str=format(Byte_Count, '012b')
                            #print(First_DW_BE_str)
                            TLP_error = line[:52]+Byte_Count_str+line[64:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)'''
                        if(j==14):
                            Requester_ID =ep_err_inj_hdl.pcie_Requester_ID_err_eij()
                            Requester_ID_str=format(Requester_ID, '16b')
                            #print(completion_Id_str)
                            TLP_error = line[:64]+Requester_ID_str+line[80:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
                        '''if(j==15):
                            Tag =ep_err_inj_hdl.pcie_Tag_err_eij()
                            Tag_Num_str=format(Tag, '08b')
                            #print(Ext_Register_Num_str)
                            TLP_error = line[:80]+Tag_str+line[88:]
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)'''
                        if(j==16):
                            Lower_Address =ep_err_inj_hdl.pcie_Lower_Address_err_eij()
                            Lower_Address_str=format(Lower_Address, '07b')
                            #print(Register_Num_str)
                            TLP_error = line[:89]+Lower_Address_str
                            err_bin_compl.write('{}\n'.format(TLP_error))
                            compl_pkt_queue.put(TLP_error)
 
                        self.k=self.k+1
                    # else statemnet: if "m"th iteration is not present in err_array then it will 0 
                    else:
                        
                        compl_pkt_queue.put(line)
                        err_bin_compl.write('{}\n'.format(line))

            else:
                
                compl_pkt_queue.put(line)
                err_bin_compl.write('{}\n'.format(line))
            self.err_id=self.err_id+1
            


        good_compl.close()

p = pcie_ep_err_call()
p.ep_err_call_fn()

err_bin_compl.close() 
error.close()


