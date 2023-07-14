from pcie_lib import *
from pcie_com_file import *
from pcie_rc_com_file import *
from pcie_rc_rx_pkt_checker import * 
from pcie_rc_com_file import ep_bad_pkts_rcvd
class pcie_rc_completion_rsp_ep_tx:
    def __init__(self):
        self.iteration = 0
        rc_to_ep_compl = open("gen_logs/rc_to_ep_compl_log.txt","w")
        rc_to_ep_compl.truncate(0)
        rc_to_ep_compl.close()

        rc_compl_sent_bin = open("gen_logs/rc_compl_sent_ep_bin.log.txt","a")
        rc_compl_sent_bin.truncate(0)
        rc_compl_sent_bin.close()
    def cmpl_rsp_from_rc_to_ep(self,ep_queue,data_payload):
        rc_compl_sent_bin = open("gen_logs/rc_compl_sent_ep_bin.log.txt","a")
        rc_to_ep_compl = open("gen_logs/rc_to_ep_compl_log.txt","a")
        str_fmt                    = ep_queue[:3]
        str_type                   = ep_queue[3:8]
        if(int(str_fmt[1], 2) == 1):
            str_fmt = format(0, '03b')
        else:
            str_fmt = format(2, '03b')
        str_t9                     = ep_queue[9]
        str_tc                     = ep_queue[9:12]
        str_t8                     = ep_queue[13]
        str_attr1                  = ep_queue[14]
        str_ln                     = ep_queue[15]
        str_th                     = ep_queue[16]
        str_td                     = ep_queue[17]
        str_ep                     = ep_queue[18]
        str_attr0                  = ep_queue[18:20]
        str_at                     = ep_queue[20:22]
        str_length                 = ep_queue[22:32]
        str_address                = ep_queue[64:94]
        str_first_dw_be            = ep_queue[60:64]
        str_completion_id = format(420, '016b')

        if(str_first_dw_be[-4:] == '0000'):         # LSB 2 bits of lower address must be as per FDB, mentioned in rev5 v1 page 173
            LA_2 = '00'
        elif(str_first_dw_be[-1] == '1'):
            LA_2 = '00'
        elif(str_first_dw_be[-2:] == '10'):
            LA_2 = '01'
        elif(str_first_dw_be[-3:] == '100'):
            LA_2 = '10'
        elif(str_first_dw_be[-4:] == '1000'):
            LA_2 = '11'
        
        completion_id = format(999, '016b')
        if self.iteration not in ep_bad_pkts_rcvd:
            str_compl_status = format(0, '03b')  # status 0 if completer succesfully sends the TLP with no error 
        else:
            str_compl_status = format(1, '03b') # status 1 if completer identifies a error in the requested TLP 
        str_bcm = format(0, '01b')               # only be set by PCI-x, so for PCIe its always 0
        str_byte_count = format(4, '012b')       # excluding memory read compl & atomic compl, byte count must be 4
        
        str_requester_id = ep_queue[32:48]     # must be same as request
        str_tag = ep_queue[48:56]              # must be same as request
        str_rsv_11_7 = format(0, '01b')          # byte 11 bit 7 is reserved
        if((str_type == '00000') & (str_fmt == '000')):  # for memory read only lower address will be calculated, mentioned in rev5 v1 page 173, 154 
            str_lower_address = str_address[-5:] + LA_2
        else:
            str_lower_address = format(0, '07b')     # excluding memory read compl & atomic compl, byte count must be 0
        
        str_payload = data_payload[::-1]

        ## TODO : Write logic faor fetching data from rc_memory
        #if(str_fmt == '010' and (str_type[1:5] in ['0000','0101'])):
        #    rc_mem.write("{}".format(hex(int(str_address,2)),hex(int(str_payload,2))))
        
        compl_pkt =  str_fmt+ str_type+ str_t9+ str_tc+ str_t8+ str_attr1+ str_ln+ str_th+ str_td+ str_ep+ str_attr0+ str_at+ str_length+ str_completion_id +str_compl_status+ str_bcm+ str_byte_count+ str_requester_id+ str_tag+ str_rsv_11_7+ str_lower_address+str_payload
         
        data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_completion_id ,str_compl_status, str_bcm, str_byte_count, str_requester_id, str_tag, str_rsv_11_7, str_lower_address,str_payload]]
        headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', 'str_payload']
        table = tabulate(data, headers=headers, tablefmt='orgtbl')
        rc_to_ep_compl.write("{}\n".format(table))
        rc_to_ep_compl.close()
        self.iteration +=1
        pkt_queue.put(compl_pkt)
        rc_compl_sent_bin.write("{}\n".format(compl_pkt))    		
        rc_compl_sent_bin.close()


#ep_tx_bin_f = open("gen_logs/ep_tx_recieved_bin.txt","r")
#line = ep_tx_bin_f.readline()
#line = line.replace("\n","")
### INFO :Erro injection using commandline arg "--err_eij=1" ##
#logging.info("ep err array---------------->{}".format.ep_err_eij_q)
#ep_tx_bin_f.close 

#c = pcie_rc_completion_rsp_ep_tx()
#c.cmpl_rsp_from_rc_to_ep
