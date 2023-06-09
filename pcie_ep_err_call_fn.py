import time
#sys.path.append('/home/shanmukh/shanmukh_cell/1_PCIe/checker_temp')
from pcie_com_file import *

from pcie_ep_err_id import *
#from ep_logs import binary_completer
from pcie_ep_field_fn import *
from pcie_final_ep_tx_table_file import *


###### Giving info about the log files###############
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_err_call_fn.py file")
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For knowing The error injected TLPs : ep_logs/err_binary_completer.txt")



'''for pkt1 in good_compl:
            
            pkt1 = pkt1.strip('\n')        
            err_bin_compl.write('priting pkt before bin compl {}\n'.format(pkt1)) ###############'''
ep_err_arr = []
err_id = {'index':0}
if(ep_err_eij): 
            while len(ep_err_arr) < ep_err_pkt_no:
                if(test == 'cfg_with_mem_seq_test'):
                    #from_index = ((num_pkts-10)//2)+10
                    from_index = 0            # error injected to both completion and request from ep
                    to_index = num_ep_pkt_tx + (((num_pkts-10)//2)+10)
                elif(test == 'cfg_test'):
                    #from_index = num_pkts
                    from_index = 0            # error injected to both completion and request from ep
                    to_index = num_ep_pkt_tx + num_pkts



                index = random.randrange(from_index, to_index)
                #err_bin_compl.write('giving error {}, total pkts {}\n'.format(index, num_pkts))
                if index not in ep_err_arr:
                    ep_err_arr.append(index)
                    #error.write('*** EP_TRANSMITTER_ERR_ID_{} ***, total pkts {} \n'.format(index, compl_qsize))                   
                ep_err_arr.sort()
            error.write('print the error list {}\n'.format(ep_err_arr))

#good_compl = open("ep_logs/binary_completer.txt","r") 
err_bin_compl = open("ep_logs/err_binary_completer.txt","w")

class pcie_ep_err_call:
    def __init__(self):
        self.k=0
        #self.err_id=0
    def ep_err_call_fn(pkt_num, pkt, err_eij):
        #compl_qsize = pkt_valid_queue.qsize()
        if(test == 'cfg_with_mem_seq_test'):                    
                    compl_qsize = num_ep_pkt_tx + (((num_pkts-10)//2)+10)
                    #print('printing completion queue size from err call function {}, error_inj is {}'.format(compl_qsize, err_eij))
        elif(test == 'cfg_test'):                    
                    compl_qsize = num_ep_pkt_tx + num_pkts
                    #print('printing completion queue size from err call function {}, error_inj is {}'.format(compl_qsize, err_eij))
        # Assuming TLP_error is a list of strings representing the rows of the table
        #num_pkts= argv.num_pkts
        TLP_error = ""
        if int(pkt, 2):
        #for num in range(compl_qsize):
            #num = (((num_pkts-10)//2)+10) + pkt_num
            #pkt = pkt.strip('\n')        
            #err_bin_compl.write('priting pkt from bin compl {}\n'.format(pkt)) ###############           
            #err_bin_compl.write('priting num okts from queue {}\n'.format(compl_qsize)) ###############
            if(err_eij):                
                if(err_id['index'] < compl_qsize):      
                    #print('num {} less than compl_qsize {} '.format(num, compl_qsize))
                    ep_err_inj_hdl = pcie_ep_field()
                    if err_id['index'] in ep_err_arr:          
                        #print('num {} in ep_err_arr '.format(num, ep_err_arr))
                        #err_bin_compl.write('priting error id {}\n'.format(num))
                        j = random.choice([4])                      
                        if(j==0):
                
                            fmt = ep_err_inj_hdl.pcie_fmt_err_eij(err_id['index'])
                            
                            fmt_str = format(fmt, '03b')       
                            #print("modified fmt->",fmt_str) 
                            TLP_error =fmt_str+pkt[3:]
                            ##compl_pkt_queue.put(TLP_error)
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            
                        # If j==0 , then "type" will be injected with error
                        if(j==1):
                            typ =ep_err_inj_hdl.pcie_type_err_eij(err_id['index'])
                            type_str=format(typ, '05b')       
                            #print(type_str) 
                            TLP_error = pkt[:3] + type_str + pkt[8:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==3):
                            TC =ep_err_inj_hdl.pcie_TC_err_eij(err_id['index'])
                            TC_str=format(TC, '03b')       
                            #print(TC_str) 
                            TLP_error = pkt[:9] + TC_str + pkt[12:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            
                            #compl_pkt_queue.put(TLP_error)
                        if(j==4):
                            Attr1 =ep_err_inj_hdl.pcie_attr1_err_eij(err_id['index'])
                            Attr1_str=format(Attr1, '01b')       
                            #print(Attr1_str) 
                            TLP_error = pkt[:13]+Attr1_str+pkt[14:] 
                            #print('err call attr1 {}, TLP {}'.format(num, TLP_error))
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==5):
                            TH =ep_err_inj_hdl.pcie_TH_err_eij(err_id['index'])
                            TH_str=format(TH, '01b')       
                            #print(TH_str)
                            #TLP_error = TH_str+pkt[:15]
                            TLP_error = pkt[:15]+TH_str+pkt[16:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==6):
                            TD =ep_err_inj_hdl.pcie_TD_err_eij(err_id['index'])
                            TD_str=format(TD, '01b')       
                            #print(TH_str)
                            #TLP_error = TH_str+pkt[:15]
                            TLP_error = pkt[:16]+TD_str+pkt[17:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==7):
                            EP =ep_err_inj_hdl.pcie_EP_err_eij(err_id['index'])
                            EP_str=format(EP, '01b')       
                            #print(EP_str) 
                            TLP_error = pkt[:17]+EP_str+pkt[18:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==8):
                            attr0 =ep_err_inj_hdl.pcie_attr0_err_eij(err_id['index'])
                            attr0_str=format(attr0, '02b')       
                            #print(attr0_str) 
                            TLP_error = pkt[:18]+attr0_str+pkt[20:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==9):
                            AT =ep_err_inj_hdl.pcie_AT_err_eij(err_id['index'])
                            AT_str=format(AT, '02b')       
                            #print(AT_str) 
                            TLP_error = pkt[:20]+AT_str+pkt[22:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        '''if(j==10):
                            length =ep_err_inj_hdl.pcie_length_err_eij(err_id['index'])
                            length_str=format(length, '10b')       
                            #print(length_str) 
                            TLP_error = pkt[:22]+length_str+pkt[32:] 
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)'''
                        if(j==11):
                            Completer_ID =ep_err_inj_hdl.pcie_Completer_ID_err_eij(err_id['index'])
                            Completer_ID_str=format(Completer_ID, '016b')
                            #print(Tag_str)
                            #TLP_error = TH_str+pkt[:15]
                            TLP_error = pkt[:32]+Completer_ID_str+pkt[48:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==11):
                            Compl_Status =ep_err_inj_hdl.pcie_Compl_Status_err_eij(err_id['index'])
                            Compl_Status_str=format(Compl_Status, '03b')
                            #print(Tag_str)
                            #TLP_error = TH_str+pkt[:15]
                            TLP_error = pkt[:48]+Compl_Status_str+pkt[51:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        if(j==12):
                            BCM =ep_err_inj_hdl.pcie_BCM_err_eij(err_id['index'])
                            BCM_str=format(BCM, '01b')
                            #print(Last_DW_BE_str)
                            #TLP_error = TH_str+pkt[:15]
                            TLP_error = pkt[:51]+BCM_str+pkt[52:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        '''if(j==13):
                            Byte_Count =ep_err_inj_hdl.pcie_Byte_Count_err_eij(err_id['index'])
                            Byte_Count_str=format(Byte_Count, '012b')
                            #print(First_DW_BE_str)
                            TLP_error = pkt[:52]+Byte_Count_str+pkt[64:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)'''
                        if(j==14):
                            Requester_ID =ep_err_inj_hdl.pcie_Requester_ID_err_eij(err_id['index'])
                            Requester_ID_str=format(Requester_ID, '16b')
                            #print(completion_Id_str)
                            TLP_error = pkt[:64]+Requester_ID_str+pkt[80:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            #compl_pkt_queue.put(TLP_error)
                        '''if(j==15):
                            Tag =ep_err_inj_hdl.pcie_Tag_err_eij(err_id['index'])
                            Tag_Num_str=format(Tag, '08b')
                            #print(Ext_Register_Num_str)
                            TLP_error = pkt[:80]+Tag_str+pkt[88:]
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            ##compl_pkt_queue.put(TLP_error)'''
                        if(j==16):
                            Lower_Address =ep_err_inj_hdl.pcie_Lower_Address_err_eij(err_id['index'])
                            Lower_Address_str=format(Lower_Address, '07b')
                            #print(Register_Num_str)
                            TLP_error = pkt[:89]+Lower_Address_str
                            #err_bin_compl.write('{}\n'.format(TLP_error))
                            ##compl_pkt_queue.put(TLP_error)
                        TLP = TLP_error
                        #err_bin_compl.write('{}\n'.format(TLP))
                        #self.k=self.k+1
                    # else statemnet: if "m"th iteration is not present in err_array then it will 0 
                    else:
                        
                        #compl_pkt_queue.put(pkt)
                        TLP = pkt
                        #err_bin_compl.write('{}\n'.format(pkt))

            else:
                
                #compl_pkt_queue.put(pkt)
                TLP = pkt
                #err_bin_compl.write('{}\n'.format(pkt))

            err_id['index'] = err_id['index'] +1
            compl_pkt_queue.put(TLP)
            err_bin_compl.write('{}\n'.format(TLP))
            pcie_final_ep_tx_table_file.pcie_final_ep_tx_table_fn(err_id['index'] - 1, TLP)




            
        

#p = pcie_ep_err_call()
#p.ep_err_call_fn()




