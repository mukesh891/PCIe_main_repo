from pcie_com_file import *
from pcie_rc_com_file import *
from tabulate import tabulate
from pcie_lib import *
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_rx_pkt_checker.py file")
from pcie_rc_memory_space import *
from pcie_rc_completion_rsp_ep_tx import *

req_queue = queue.Queue()
tag_queue = queue.Queue()
# creating file for completion id check #
rc_checker_f = open("gen_logs/rc_checker_log.txt","w")
rc_to_ep_compl = open("gen_logs/rc_to_ep_compl_log.txt","w")
#ep_tx_rc = open("ep_logs/ep_tx_send_pkt_bin.txt","r")
from pcie_rc_driver import rc_error_count_for_write_mem
from pcie_rc_config_space_type0 import *

print(RCB)
cfg_space = rc_cfg_space_type0()
compl_rsp = pcie_rc_completion_rsp_ep_tx()
class pcie_rc_rx_pkt_checker:#(pcie_seq_rc_config_pkt):
    def __init__(self):
        #ep_err_eij_q =[]
        self.iteration = 0
        self.good_pkts = 0
        self.ep_gen_good_pkts= 0
        self.bad_pkts =0
        self.ep_gen_bad_pkts= 0
        self.ep_cfg_read_req_pkts_rcvd = 0
        self.ep_cfg_write_req_pkts_rcvd = 0
        self.ep_mem_read_req_rcvd = 0
        self.ep_mem_write_req_rcvd = 0
        self.ep_pkts_iter = 0
        self.ep_err_pkt_no_arr = []
        self.compl_err_pkts = []
        self.ep_err_pkt_no_arr_with_compl = []

        self.read_from_addr=0

        ep_tx_bin_f = open("gen_logs/ep_tx_recieved_bin.txt","w")
        ep_tx_bin_f.truncate(0)
        ep_tx_bin_f.close()
        rc_mem_f = open("gen_logs/rc_ep_side_pkt_recieved_memory.txt","w")
        rc_mem_f.truncate(0)
        rc_mem_f.close()


    def rc_rx_checker(self):
        rc_mem_f = open("gen_logs/rc_ep_side_pkt_recieved_memory.txt","a")
        
        global packet_numbers
        bin_f = open("gen_logs/rc_mem_bin_file.txt","r")
        ep_tx_bin_f = open("gen_logs/ep_tx_recieved_bin.txt","a")
        
        
        # loop for reading values from compl_pkt_queue #
        #for i in range(compl_pkt_queue.qsize()):
        
        for line in bin_f: 

            requester_st  = line[32:48]
            tag_st  = line[48:56]
            req_queue.put(requester_st) 
            tag_queue.put(tag_st) 
        if compl_pkt_queue.qsize() > 0:
            rc_checker_f.write('\nqsize from completion is {}\n'.format(compl_pkt_queue.qsize()))
            ep_queue = compl_pkt_queue.get()
            if ep_queue:
                #logger.info("{}\n".format(ep_queue))
            #for i in range(compl_pkt_queue.qsize()):       
                # ep_queue is a string type -> reading data from compl_queue #
                #ep_queue = compl_pkt_queue.queue[i] 
                # assgning all filed value from ep_queue #
                str_fmt                    = ep_queue[:3]         
                str_type                   = ep_queue[3:8]        
                str_t9                     = ep_queue[8]          
                str_tc                     = ep_queue[9:12]       
                str_t8                     = ep_queue[12]         
                str_attr1                  = ep_queue[13]         
                str_ln                     = ep_queue[14]         
                str_th                     = ep_queue[15]         
                str_td                     = ep_queue[16]         
                str_ep                     = ep_queue[17]         
                str_attr0                  = ep_queue[18:20]      
                str_at                     = ep_queue[20:22]      
                str_length                 = ep_queue[22:32]      
                
                
                def completion_recieved(ep_queue):
                    if str_type == '01010':
                 
                        str_completion_id          = ep_queue[32:48]   
                        str_compl_status           = ep_queue[48:51]   
                        str_bcm                    = ep_queue[52]      
                        str_byte_count             = ep_queue[52:64]   
                        str_requester_id           = ep_queue[64:80]   
                        str_tag                    = ep_queue[80:88]   
                        str_reserved_r             = ep_queue[88]      
                        #print(str_reserved_r)                         
                        str_lower_address          = ep_queue[89:96]   
                        temp_payload = ep_queue[96:]
                                                                       
                        # printing header for rc_checker_log.txt file #
                        rc_checker_f.write("-------------------------------------------------------------------------- TLP ")
                        rc_checker_f.write(str(packet_numbers))
                        rc_checker_f.write(" ------------------------------------------------------------------------- ")
                        rc_checker_f.write("\n")
                        rc_checker_f.write('\nCompletion packet recieved -> {}\n'.format(ep_queue))
                        if(len(temp_payload) % 32 == 0):
                            payload_size_recieved = len(temp_payload) // mps
                            if (len(temp_payload) <= mps*32):
                                rc_checker_f.write("VALID Payload Recieved within the mps of {}DW\n".format(mps))
                                str_payload = temp_payload
                            else:
                                rc_checker_f.write("INVALID Payload Recieved : mps out of bound i.e {}DW, payload : {}\n".format(payload_size_recieved,temp_payload))
                                str_payload = temp_payload

                        else:
                            rc_checker_f.write("INVALID Payload Recieved with SIZE of {} i.e unalligned data\n".format(len(temp_payload)))
                            logger.error("INVALID Payload Recieved with length of {} i.e unalligned data, It must be with in {}\n".format(len(temp_payload),mps*32))
                            str_payload = temp_payload
                        
                        # Checking all the completer fields for validation and range format #
                        #if ((line[0:3] == '000' and str_fmt[0:3] == '010') or ((line[0:3]) == '010' and str_fmt[0:3] == '000')): # ep completer: fmt will be 0 or 2
                        if (str_fmt[0:3] == '010') or (str_fmt[0:3] == '000'): # ep completer: fmt will be 0 or 2
                            #print("VALID fmt RECIEVED")
                            if int(str_type        ,2) in [10]:
                                #if int(str_type        ,2) in [10] and str_fmt == '010':         # ep completer: will be 10
                                #    rc_checker_f.write("MEMORY READ request MemRD \n")
                                #    mem_read_req_compl_rcvd = mem_read_req_compl_rcvd + 1 
                                #elif int(str_type        ,2) in [10] and str_fmt == "010":         # ep completer: will be 10
                                #    rc_checker_f.write("CONFIG READ request CfgRD \n")
                                #    cfg_read_req_compl_pkts_rcvd = cfg_read_req_compl_pkts_rcvd +1 
                                #elif int(str_type        ,2) in [10] and str_fmt == "000":         # ep completer: will be 10
                                #    rc_checker_f.write("CONFIG WRITE request CfgWR \n")  
                                #    cfg_write_req_compl_pkts_rcvd = cfg_write_req_compl_pkts_rcvd + 1
                                if int(str_t9,2) == 0:                  # ep completer:t9 must be 0
                                    if int(str_tc          ,2) == 0:    # ep completer: tc will be 0 for time being
                                        if int(str_t8,2) == 0:          # ep completer: t8 will be 10
                                            if int(str_attr1       ,2) == 0:            # ep completer:attr1 will be 0                   
                                                if int(str_ln,2) == 0:                  # ep completer:ln must be 0
                                                    if int(str_th          ,2) == 0:    # ep completer: th will be 0 for time being
                                                        if int(str_td          ,2) == 0:                # ep completer: td will be 0
                                                            if int(str_ep          ,2) == 0:            # ep completer: ep must be 0
                                                                if int(str_attr0       ,2) == 0:        # ep completer: attr0 will be 0 
                                                                    if int(str_at          ,2) == 0:    # ep completer: at will be 0
                                                                        if int(str_length      ,2) ==1:                                # ep completer: length will be 1
                                                                            if int(str_completion_id        ,2) in range(0,2**16-1):    # ep completer: commpleter id must be greater than 0
                                                                                if int(str_compl_status                 ,2) == 0:      # ep completer: completer status must be 1 for pass adn 0 for fail packet
                                                                                    if int(str_bcm          ,2) == 0:                  # ep completer: bcm will be 0
                                                                                        if int(str_byte_count         ,2) in range(0,2**12-1):       # ep completer: byte_count must be within range 0 to 2**12-1
                                                                                            if str_requester_id  in req_queue.queue:     # ep completer: requester_id must be same as generated requester id
                                                                                                if str_tag in tag_queue.queue:                   # ep completer: tag will be within range 0 to 2**8-1
                                                                                                    if int(str_reserved_r,2) == 0:           # ep completer: reserved_bit will be 0 
                                                                                                        #print("reserved_bit--------->",str_reserved_r)
                                                                                                        if (int(str_lower_address             ,2)>0) in range(0,2**7-1): # ep completer: lower_address will be within 0 to 2**7-1
                 
                                                                                                            #rc_checker_f.write("fmt = ")
                                                                                                            #rc_checker_f.write(hex(int(str_fmt,2))) 
                                                                                                            #rc_checker_f.write("\n")                        
                                                                                                            #rc_checker_f.write("type = ")
                                                                                                            #rc_checker_f.write(hex(int(str_type,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("t9 = ")
                                                                                                            #rc_checker_f.write(hex(int(str_t9,2)))       
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("tc = ")
                                                                                                            #rc_checker_f.write(hex(int(str_tc,2       )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("t8 = ")
                                                                                                            #rc_checker_f.write(hex(int(str_t8,2)))       
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("attr1 = ")
                                                                                                            #rc_checker_f.write(hex(int(str_attr1,2       )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("ln = ")
                                                                                                            #rc_checker_f.write(hex(int(str_ln,2)))      
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("th = ")  
                                                                                                            #rc_checker_f.write(hex(int(str_th,2          )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("td = ")  
                                                                                                            #rc_checker_f.write(hex(int(str_td,2          )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("ep = ") 
                                                                                                            #rc_checker_f.write(hex(int(str_ep,2          )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("attr0 = ")
                                                                                                            #rc_checker_f.write(hex(int(str_attr0,2       )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("at = ")
                                                                                                            #rc_checker_f.write(hex(int(str_at,2          )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("length = ")
                                                                                                            #rc_checker_f.write(hex(int(str_length,2      )))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("completer_id = ")
                                                                                                            #rc_checker_f.write(hex(int(str_completion_id,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("compl_status = ")
                                                                                                            #rc_checker_f.write(hex(int(str_compl_status,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("bcm = ")
                                                                                                            #rc_checker_f.write(hex(int(str_bcm,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("byte_count = ")
                                                                                                            #rc_checker_f.write(hex(int(str_byte_count,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("requester_id = ")
                                                                                                            #rc_checker_f.write(hex(int(str_requester_id,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("tag = ")
                                                                                                            #rc_checker_f.write(hex(int(str_tag,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write("lower_address = ")
                                                                                                            #rc_checker_f.write(hex(int(str_lower_address,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            #rc_checker_f.write(hex(int(str_payload,2)))
                                                                                                            #rc_checker_f.write("\n")
                                                                                                            self.good_pkts=self.good_pkts+1
                                                                                                             
                                                                                                        else:
                                                                                                            rc_checker_f.write("INVALID LOWER_ADDRESS RECIEVED: lower_address CANNOT BE NEGATIVE [Note : Please check and declare the value, VALUE RECIEVED : {}".format(int(str_lower_address,2)))
                                                                                                            self.compl_err_pkts.append(self.iteration)
                 
                 
                                                                                                    # reserved_r else
                                                                                                    else:
                                                                                                        rc_checker_f.write("INVALID RESERVE_R RECIEVED: reserved_r CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of reserve_bit r as 0 (as it is unused), VALUE RECIEVED : {}\n\n".format(int(str_reserved_r,2)))
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.compl_err_pkts.append(self.iteration)
                 
                                                                                                ## tag else
                                                                                                else:
                                                                                                    rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 2**8-1 [Note : Please check and assign the value with in the range(0,2**8-1), VALUE RECIEVED : {}\n\n".format(int(str_tag,2)))
                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                    self.compl_err_pkts.append(self.iteration)
                                                                                            #completer_id else
                                                                                            else:
                                                                                                rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1), VALUE RECIEVED : {}\n\n".format(int(str_requester_id,2)))
                                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                self.compl_err_pkts.append(self.iteration)
                                                                                        #byte_count else
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID BYTE_COUNT RECIEVED: byte_count CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**12-1), VALUE RECIEVED : {}\n\n".format(int(str_byte_count,2)))
                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                            self.compl_err_pkts.append(self.iteration)
                                                                                    #last_dw_be else
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID BCM RECIEVED: bcm CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**4-1), VALUE RECIEVED : {}\n\n".format(int(str_bcm,2)))                                                                               
                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                        self.compl_err_pkts.append(self.iteration)
                                                                                #tag else
                                                                                else:
                                                                                    rc_checker_f.write("INVALID COMPL_STATUS RECIEVED: compl_status CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,2**8-1), VALUE RECIEVED : {}\n\n".format(int(str_compl_status,2)))
                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                    self.compl_err_pkts.append(self.iteration)
                                                                            #completer_id else
                                                                            else:
                                                                                rc_checker_f.write("INVALID COMPLETER_ID RECIEVED: completion_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1), VALUE RECIEVED : {}\n\n".format(int(str_completion_id,2)))
                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                self.compl_err_pkts.append(self.iteration)
                                                                        #length else
                                                                        else:
                                                                            rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 2**10-1 [Note : Please check and assign the value with in the range(0,2**10-1), VALUE RECIEVED : {}\n\n".format(int(str_length,2)))
                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                            self.compl_err_pkts.append(self.iteration)
                                                                    #at else
                                                                    else:
                                                                        rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 2**2-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                        self.compl_err_pkts.append(self.iteration)
                                                                #attr0 else
                                                                else:
                                                                    rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}\n\n".format(int(str_at,2)))
                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                    self.compl_err_pkts.append(self.iteration)
                                                            #ep else
                                                            else:
                                                                rc_checker_f.write("INVALID EP RECIEVED: ep CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}\n\n".format(int(str_ep,2)))
                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                self.compl_err_pkts.append(self.iteration)
                                                        #td else
                                                        else:
                                                            rc_checker_f.write("INVALID TD RECIEVED: td CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}\n\n".format(int(str_td,2)))
                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                            self.compl_err_pkts.append(self.iteration)
                                                    #th else
                                                    else:
                                                        rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}\n\n".format(int(str_th,2)))
                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                        self.compl_err_pkts.append(self.iteration)
                                                                                                
                                                ## ln else
                                                else:
                                                    rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of ln as 0 (as it is unused), VALUE RECIEVED : {}\n\n".format(int(str_type,2)))
                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                    self.compl_err_pkts.append(self.iteration)
                                            ## attr1 else
                                            else:
                                                rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}\n\n".format(int(str_ln,2)))
                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                self.compl_err_pkts.append(self.iteration)
                 
                                        ## t8 else
                                        else:
                                            rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t8 as 0 (as it is unused), VALUE RECIEVED : {}\n\n".format(int(str_t8,2)))
                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                            self.compl_err_pkts.append(self.iteration)
                                    ## tc else
                                    else:
                                        rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,7), VALUE RECIEVED : {}\n\n".format(int(str_tc,2)))
                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                        self.compl_err_pkts.append(self.iteration)
                                ## t9 else
                                else:
                                    rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t9 as 0 (as it is unused), VALUE RECIEVED : {}\n\n".format(int(str_t9,2)))
                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                    self.compl_err_pkts.append(self.iteration)
                            ## type else
                            else:
                                rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 31 [Note : Please check and assign the value with in the range(0,2**5-1), VALUE RECIEVED : {}\n\n".format(int(str_type,2)))
                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                self.compl_err_pkts.append(self.iteration)
                        ## fmt else
                        else:
                            rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,2**3-1), VALUE RECIEVED : {}\n\n".format(int(str_fmt,2)))
                            self.bad_pkts=self.bad_pkts+1                                                                                                
                            self.compl_err_pkts.append(self.iteration)
                 
                        
                        data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_completion_id ,str_compl_status, str_bcm, str_byte_count, str_requester_id, str_tag, str_reserved_r, str_lower_address,str_payload]]
                        headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', 'str_payload']
                        table = tabulate(data, headers=headers, tablefmt='orgtbl')
                        rc_checker_f.write("{}\n\n\n".format(table)) 
                        rc_checker_f.write("GOOD_PKTS RECIEVED ={}\n".format(str(self.good_pkts)))
                        rc_checker_f.write("BAD_PKT RECIEVED ={}\n\n\n".format(str(self.bad_pkts)))
                 
                def ep_tx_recieved(ep_queue):
                    #with open("ep_logs/ep_tx_send_pkt_bin.txt","r") as ep_tx_rc: 
                        #cpl_queue = ep_tx_rc.readline()
                        #logger.info("RC_rx_checker side recievd pkts -> {}".format(ep_tx_rc.readline()))
                    cpl_queue = ep_queue
                    if cpl_queue:
                        #logger.info("{}\n".format(cpl_queue))
                        cpl_queue  = cpl_queue.replace("\n","")
                        compl_st = None 
                        str_fmt                    = cpl_queue[:3]         
                        str_type                   = cpl_queue[3:8]        
                        str_t9                     = cpl_queue[8]          
                        str_tc                     = cpl_queue[9:12]       
                        str_t8                     = cpl_queue[12]         
                        str_attr1                  = cpl_queue[13]         
                        str_ln                     = cpl_queue[14]         
                        str_th                     = cpl_queue[15]         
                        str_td                     = cpl_queue[16]         
                        str_ep                     = cpl_queue[17]         
                        str_attr0                  = cpl_queue[18:20]      
                        str_at                     = cpl_queue[20:22]      
                        str_length                 = cpl_queue[22:32]   
                        if str_type in ['00101' , '00000']:
                            ##forcimg td bit to 0 need to delete it later
                            str_td = '0'
                            
                            ep_tx_bin_f.write("{}\n".format(cpl_queue))
                 
                            rc_checker_f.write("-------------------------------------------------------------------------- TLP {} -------------------------------------------------------------------------\n".format(str(packet_numbers)))
                            rc_checker_f.write('\nEP generated packet recieved -> {}\n'.format(cpl_queue))
                            str_requester_id = cpl_queue[32:48]             
                            str_tag = cpl_queue[48:56]                      
                            str_last_dw_be = cpl_queue[56:60]                   
                            str_first_dw_be = cpl_queue[60:64]                  
                            lower_address = cpl_queue[89:96] 
                                                                           
                            if (str_type[2] == '1'):                      
                                str_completion_id = cpl_queue[64:80]           
                                str_rsv_10_7 = cpl_queue[80:84]               
                                str_ext_register_num = cpl_queue[84:88]        
                                str_register_num = cpl_queue[88:94]            
                                str_rsv_11_1 = cpl_queue[94:96]               

                            elif(str_type[0:4] == '0000'):                   
                                str_address = cpl_queue[64:94]                 
                                str_rsv_11_1 = cpl_queue[94:96]                 
                            
                            if(int(str_td,2)):
                                str_payload= cpl_queue[96:len(cpl_queue)-32]               
                                str_ecrc = cpl_queue[len(cpl_queue)-32:]              
                                tlp_packet_without_ecrc  = cpl_queue[:len(cpl_queue)-32]
                                integer_tlp_value = int(tlp_packet_without_ecrc , 2)
                                ecrc_divisor = int(fixed_ecrc_divisor, 2)
                                integer_ecrc_value = integer_tlp_value % ecrc_divisor 
                                #remainder = integer_value % fixed_integer_value
                                ecrc_value = bin(integer_ecrc_value)[2:].zfill(32)
                                #print("----------------->",str_ecrc, ecrc_value)
                                if(ecrc_value == str_ecrc):
                                    logger.info("EP ecrc value MISMATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(cpl_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                                    rc_checker_f.write("EP ecrc value MATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(cpl_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                                else:
                                    rc_checker_f.write("ERROR : EP ecrc value MISMATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(cpl_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                                    #logger.error("EP ecrc value MISMATCHES with calculated ecrc value : EP ECRC : {} , CALCULATED ECRC : {} \n".format(int(ecrc_value,2) , int(str_ecrc,2)))
                             
                            else:
                                str_payload= cpl_queue[96:]               

                 
                            if(len(str_payload)%32 == 0):
                                pass
                            else:
                                logger.error("PAYLOAD SIZE IS UNALLIGNED, LENGTH OF PAYLOAD IS : {}".format(len(str_payload)))
                 
                            ##
                            if (str_fmt[0:3] in ['010','000']): 
                                #print("VALID fmt RECIEVED")
                                if int(str_type        ,2) in [0,5]:
                                    #logger.info("----------------------->ep_tx_recieved with fmt = {} and type = {}".format(str_fmt,str_type))
                                    if int(str_type        ,2) in [0] and str_fmt[:3] == "000":         # ep completer: will be 10
                                        rc_checker_f.write("MEMORY READ request MemRD \n")
                                        self.ep_mem_read_req_rcvd = self.ep_mem_read_req_rcvd + 1 
                                    elif int(str_type        ,2) in [0] and str_fmt[:3] == "010":         # ep completer: will be 10
                                        rc_checker_f.write("MEMORY WRITE request MemWR \n")
                                        self.ep_mem_write_req_rcvd = self.ep_mem_write_req_rcvd + 1 
                                    elif int(str_type        ,2) in [5] and str_fmt[:3] == "000":         # ep completer: will be 10
                                        rc_checker_f.write("CONFIG READ request CfgRD \n")
                                        self.ep_cfg_read_req_pkts_rcvd = self.ep_cfg_read_req_pkts_rcvd +1 
                                    elif int(str_type        ,2) in [5] and str_fmt[:3] == "010":         # ep completer: will be 10
                                        rc_checker_f.write("CONFIG WRITE request CfgWR \n")  
                                        self.ep_cfg_write_req_pkts_rcvd = self.ep_cfg_write_req_pkts_rcvd + 1
                                    if int(str_t9,2) == 0:                  # ep completer:t9 must be 0
                                        if int(str_tc          ,2) == 0:    # ep completer: tc will be 0 for time being
                                            if int(str_t8,2) == 0:          # ep completer: t8 will be 10
                                                if int(str_attr1       ,2) == 0:            # ep completer:attr1 will be 0                   
                                                    if int(str_ln,2) == 0:                  # ep completer:ln must be 0
                                                        if int(str_th          ,2) == 0:    # ep completer: th will be 0 for time being
                                                            if int(str_td          ,2) in  [0]:                # ep completer: td will be 0
                                                                if int(str_ep          ,2) in [0,1]:            # ep completer: ep must be 0
                                                                    if int(str_attr0       ,2) == 0:        # ep completer: attr0 will be 0 
                                                                        if int(str_at          ,2) == 0:    # ep completer: at will be 0
                                                                            if int(str_length      ,2) < 2**10:                                # ep completer: length will be 1 or greater than 1
                                                                                if int(str_requester_id      ,2) < 2**16 :                                # ep completer: str_requester_id will be > 0
                                                                                    if int(str_tag      ,2) < 2**8 :                                # ep completer: length will be 1
                                                                                        if int(str_last_dw_be      ,2) < 2**4 :                                # ep completer: str_last_dw_be will be 0 for length = 1 else random value
                                                                                            if int(str_first_dw_be      ,2) < 2**4 :                                # ep completer: str_last_dw_be length will be >0 for any tx
                                                                                                if (str_type[2] == '1'):                     
                                                                                                    if int(str_completion_id      ,2) == 0 :                                # ep completer: length will be 1
                                                                                                        if int(str_rsv_10_7      ,2) == 0 :                                # ep completer: length will be 1
                                                                                                            if int(str_ext_register_num      ,2) >= 0 :                                # ep completer: length will be 1
                                                                                                                if int(str_register_num      ,2) >= 0 :                                # ep completer: length will be 1
                                                                                                                    if int(str_rsv_11_1      ,2) == 0 :                                # ep completer: length will be 1
                                                                                                                        self.good_pkts = self.good_pkts + 1
                                                                                                                        self.ep_gen_good_pkts=self.ep_gen_good_pkts+1
                                                                                                                        ep_good_pkts_rcvd.append(self.ep_pkts_iter)
                                                                                                                        compl_st = str(0)
                                                                                                                        #if int(str_type        ,2) in [0] and str_fmt[:3] == "010":           # ep completer: will be 10
                                                                                                                        #    ## TODO : No Completion will be sent instead the data will be written to mem_space
                                                                                                                        #    write_modify_data(address,data,length)
                                                                                                                        #elif int(str_type        ,2) in [0] and str_fmt[:3] == "000":           # ep completer: will be 10
                                                                                                                        #    ## TODO : Completion will be sent from mem
                                                                                                                        #    read_data_from_mem_space(address, length)
                                                                                                                        if int(str_type        ,2) in [5] and str_fmt[:3] == "010":         # ep completer: will be 10
                                                                                                                            #logger.info("PAYLOAD writing to config space IS-----------> {} str td = {} ".format(str_payload,str_td))
                                                                                                                            cfg_space.write_cfg(cpl_queue, str_payload, self.ep_pkts_iter, compl_st)
                                                                                                                            self.read_from_addr =self.ep_pkts_iter 
                                                                                                                           ## TODO : Completion will be sent from config
                                                                                                                        elif int(str_type        ,2) in [5] and str_fmt[:3] == "000":         # ep completer: will be 10
                                                                                                                            #str_payload = cfg_space.read_cfg(cpl_queue, str_payload, self.ep_pkts_iter, compl_st)
                                                                                                                            data_payload = cfg_space.read_cfg(cpl_queue, str_payload, self.read_from_addr, compl_st)
                                                                                                                            #logger.info("PAYLOAD reading from cfg space IS-----------> {} str td = {} ".format(str_payload,str_td))
  
                 
                                                                                                                    else:
                                                                                                                        rc_checker_f.write("INVALID str_rsv_11_1 RECIEVED: rsv_11_1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_rsv_11_1,2)))
                                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                                else:
                                                                                                                    rc_checker_f.write("INVALID REGISTER_NUMBER RECIEVED: register_num CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_register_num,2)))
                                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                                    ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                            else:
                                                                                                                rc_checker_f.write("INVALID EXT_REGISTER_NUMBER RECIEVED: ext_register_num CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_ext_register_num,2)))
                                                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                        else:
                                                                                                            rc_checker_f.write("INVALID rsv_10_7 RECIEVED: rsv_10_7 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_rsv_10_7,2)))
                                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                    else:
                                                                                                        rc_checker_f.write("INVALID COMPLETION_ID RECIEVED: completion_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)] VALUE RECIEVED : {}\n\n".format(int(str_completion_id,2)))
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                                        
                                                                                                elif(str_type[0:4] == '0000'):
                                                                                                    if int(str_address      ,2) < 2**30 :                                # ep completer: length will be 1
                                                                                                        if int(str_rsv_11_1      ,2) == 0  :                                # ep completer: length will be 1
                                                                                                            if(str_fmt == '010'):

                                                                                                                self.good_pkts = self.good_pkts + 1
                                                                                                                self.ep_gen_good_pkts=self.ep_gen_good_pkts+1
                                                                                                                ep_good_pkts_rcvd.append(self.ep_pkts_iter)
                                                                                                                data = str_payload[::-1]
                                                                                                                rc_mem_f.write("Address: {}\t Data: {}\n".format(str_address,data)) 
                                                                                                                offset = lower_address
                                                                                                                if(mps > int(str_length,2)):
                                                                                                                    write_modify_data(str_address,data,str_length)
                                                                                                                else:
                                                                                                                    write_modify_data(str_address,data,bin(mps))
                                                                                                                    

                                                                                                                for i in range(mps):
                                                                                                                    offset_int = int(offset,2)+(4*i)
                                                                                                                    #offset = offset+(i*4) #address with 4 byte allignment
                                                                                                                    for j in range(4):
                                                                                                                        offset_hex = hex(offset_int).upper() 
                                                                                                                        data_bin = data[j*8:(j+1)*8]
                                                                                                                        data_hex = hex(int(data_bin,2)).upper()
                                                                                                                        data_hex_0 = "{}".format(hex(int(data_bin,2)).upper())
                                                                                                                        rc_mem_f.write(f"Offset: {offset_hex}\t Data: {data_hex}\n")
                                                                                                                        offset_int += 1
                                                                                                            elif(str_fmt == '000'):
                                                                                                                logger.info("+++++++++++++++++++++ENTERING THE READ TX LOOP AT RC SIDE ++++++++++++++++++++++")
                                                                                                                if(int(str_payload,2)==0):
                                                                                                                    pass
                                                                                                                else:
                                                                                                                    rc_checker_f.write("INVALID PAYLOAD RECIEVED: PAYLOAD CANNOT BE ASSIGNED DURING THE TIME OF MEMORY READ TX: RECIEVED PAYLOAD : {}\n\n".format(int(str_payload,2)))
                                                                                                                ## TODO : Completion will be sent from mem
                                                                                                                        
                                                                                                                length = int(str_length,2)
                                                                                                                if length % RCB == 0:
                                                                                                                    num_compl_tx = length // RCB 
                                                                                                                else:
                                                                                                                    num_compl_tx = ( length // RCB ) +1
                                                                                                                    remaining_len =  length % RCB 
                                                                                                                #num_compl_tx = (RCB*32) // len(str_payload)
                                                                                                                # uncomment to enable RCB feature:
                                                                                                                for k in range(num_compl_tx):
                                                                                                                    if (length > RCB):
                                                                                                                        read_length = bin(RCB)[2:]
                                                                                                                    else:
                                                                                                                        read_length = bin(remaining_len)[2:]
                                                                                                                # TODO : Completion will be sent from mem
                                                                                                                    data_payload = read_data_from_mem_space(str_address, read_length)
                                                                                                                    compl_rsp.cmpl_rsp_from_rc_to_ep(cpl_queue, data_payload)
                                                                                                                    
                                                                                                                    length -= RCB
                                                                                                                    str_address = bin((int(str_address,2)+RCB))[2:]
                                                                                                        # else :str_rsv_11_1      
                                                                                                        else:
                                                                                                            rc_checker_f.write("INVALID rsv_11_1 RECIEVED: rsv_11_1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_rsv_11_1,2)))
                                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                             
                                                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                    # else :str_address      
                                                                                                    else:
                                                                                                        rc_checker_f.write("INVALID ADDRESS RECIEVED: address CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_address,2)))
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1
                                                                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                            # else :str_first_dw_be
                                                                                            else:
                                                                                                rc_checker_f.write("INVALID FIRST_DW_BE RECIEVED: first_dw_be CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_first_dw_be,2)))
                                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                        # else :str_last_dw_be
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID LAST_DW_BE RECIEVED: last_dw_be CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_last_dw_be,2)))
                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                    # else :str_tag
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_tag,2)))
                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                # else :str_requester_id
                                                                                else:
                                                                                    rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_requester_id,2)))
                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                    ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                            # else :str_length
                                                                            else:
                                                                                rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_length,2)))
                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                        # else :str_at
                                                                        else:
                                                                            rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_at,2)))
                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                    # else :str_attr0
                                                                    else:
                                                                        rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_attr0,2)))
                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                # else :str_ep
                                                                else:
                                                                    rc_checker_f.write("INVALID EP RECIEVED: ep CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_ep,2)))
                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                    ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                            # else :str_td
                                                            else:
                                                                rc_checker_f.write("INVALID TD RECIEVED: td CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_td,2)))
                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                        # else :str_th
                                                        else:
                                                            rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_th,2)))
                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                    # else :str_ln
                                                    else:
                                                        rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_ln,2)))
                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                # else :str_attr1
                                                else:
                                                    rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_attr1,2)))
                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                    ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                            # else :str_t8
                                            else:
                                                rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_t8,2)))
                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                        # else :str_tc
                                        else:
                                            rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 7 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}\n\n".format(int(str_tc,2)))
                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                            ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                    # else :str_t9
                                    else:
                                        rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}\n\n".format(int(str_t9,2)))
                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                        ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                # else :str_type
                                else:                                                                                    
                                    rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 15 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}\n\n".format(int(str_type,2)))
                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                    ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                            # else :str_fmt
                            else:
                                rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 7 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}\n\n".format(int(str_type,2)))
                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                ep_bad_pkts_recieved.append(self.ep_pkts_iter)
                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                                     
                 
                 
                            
                            if (str_type[2] == '1'):                      
                                data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be,  str_completion_id ,str_rsv_10_7, str_ext_register_num, str_register_num, str_rsv_11_1,str_payload]]
                                headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Requester_Id', 'Tag', ' last_dw_be' ,'first_dw_be', 'Completion_Id', 'rsv_10_7','ext_register_num', 'str_register_num', 'str_rsv_11_1','str_payload']
                                table = tabulate(data, headers=headers, tablefmt='orgtbl')
                                rc_checker_f.write(table) 
                 
                            elif(str_type[0:4] == '0000'):                   
                                data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be, str_address, str_rsv_11_1,str_payload]]
                                headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Requester_Id', 'Tag', ' last_dw_be' ,'first_dw_be', 'str_address', 'str_rsv_11_1','str_payload']
                                table = tabulate(data, headers=headers, tablefmt='orgtbl')
                                rc_checker_f.write(table) 
                            rc_checker_f.write("\n\n\n")                    
                            rc_checker_f.write("GOOD_PKTS RECIEVED = {}\n".format(str(self.good_pkts)))
                            rc_checker_f.write("BAD_PKT RECIEVED = {}\n".format(str(self.bad_pkts)))
                            rc_checker_f.write("self.ep_cfg_read_req_pkts_rcvd = {}\n".format(str(self.ep_cfg_read_req_pkts_rcvd)))
                            rc_checker_f.write("self.ep_cfg_write_req_pkts_rcvd = {}\n".format(str(self.ep_cfg_write_req_pkts_rcvd)))
                            rc_checker_f.write("self.ep_mem_read_req_rcvd = {}\n".format(str(self.ep_mem_read_req_rcvd)))
                            rc_checker_f.write("self.ep_mem_write_req_rcvd = {}\n".format(str(self.ep_mem_write_req_rcvd)))
                            rc_checker_f.write("total good packets from EP generator side = {}\n".format(str(self.ep_gen_good_pkts)))
                            rc_checker_f.write("total error/bad packets from EP generator side = {}\n".format(str(self.ep_gen_bad_pkts)))
                            rc_checker_f.write("\n\n\n")
                            self.ep_pkts_iter = self.ep_pkts_iter+1
                            total_pkts_from_ep =self.ep_cfg_read_req_pkts_rcvd + self.ep_cfg_write_req_pkts_rcvd + self.ep_mem_read_req_rcvd + self.ep_mem_write_req_rcvd
                            if(total_pkts_from_ep == num_ep_pkt_tx):
                                rc_checker_f.write("total_pkts_from_ep = {}\n".format(str(total_pkts_from_ep)))
                                logger.info("Total packets transmitted from EP side matches with total packet recieved et RC side: EP num pkts: {} , RC recieved num pkts: {}\n".format(str(total_pkts_from_ep),str(num_ep_pkt_tx)))
                        #else:
                        #    logger.error("Total packets transmitted from EP side doesnt matcthes with total packet recieved et RC side: EP num pkts: {} , RC recieved num pkts: {}\n".format(str(total_pkts_from_ep),str(num_ep_pkt_tx)))
                         
                        final_err_eij = err_pkt_no - rc_error_count_for_write_mem
                        rc_checker_f.write("RC_error_injected = err_pkt_no : {}\n".format(str(err_pkt_no)))  
                        rc_checker_f.write("NOTE : There may be error injection to the write mem req(MemWR) at RC side, So we dont get any completion for it so we need to neglect the MemWR error injection i.e -> \n final RC_error_injection = err_pkt_no - rc_error_count_for_write_mem : {}\n".format(str(final_err_eij))) 
                         
                         
                        rc_checker_f.write("RC error injected pkts with completion status : {}\n".format(str(self.compl_err_pkts)))  
                        rc_checker_f.write("EP error injected pkts are : {}\n".format(str(self.ep_err_pkt_no_arr)))  
                        rc_checker_f.write("EP error injected pkts are : {}\n".format(str(ep_bad_pkts_rcvd)))  
                        rc_checker_f.write("EP error injected pkts with completion packets : {}\n".format(str(self.ep_err_pkt_no_arr_with_compl)))  
                        #ep_tx_rc.close() 
                     
                    self.iteration += 1
                    __all__ = ['self.ep_err_pkt_no_arr']
                
                    def send_completion_to_ep_tlp(self,ep_queue, data_payload):
                        #data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be,  str_completion_id ,str_rsv_10_7, str_ext_register_num, str_register_num, str_rsv_11_1]]
                        c_fmt                    = ep_queue[:3]
                        if(int(c_fmt[1], 2) == 1):
                            compl_fmt = format(0, '03b')
                        else:
                            compl_fmt = format(2, '03b')

                        compl_type                   = format(10,'05b')#
                        if (compl_type[0:4] == '0000' and compl_fmt == '000') or (compl_type[2] == '1' and (compl_fmt in ['000','010']) ):
                            compl_t9                     = ep_queue[9]          
                            compl_tc                     = ep_queue[9:12]       
                            compl_t8                     = ep_queue[12]         
                            compl_attr1                  = ep_queue[13]         
                            compl_ln                     = ep_queue[14]         
                            compl_th                     = ep_queue[15]         
                            compl_td                     = ep_queue[16]         
                            compl_ep                     = ep_queue[17]         
                            compl_attr0                  = ep_queue[18:20]      
                            compl_at                     = ep_queue[20:22]      
                            compl_length                 = ep_queue[22:32]      
                            compl_completion_id          = format(0x00ff,'016b')   
                            compl_compl_status           = format(0,'03b')
                            compl_bcm                    = format(0,'01b')      
                            compl_byte_count             = format(4,'012b')   
                            compl_requester_id           = ep_queue[32:48]  
                            compl_tag                    = ep_queue[48:56]   
                            compl_reserved_r             = format(0,'01b') 
                            compl_lower_address          = ep_queue[89:96]
                            read_addr                    = ep_queue[64:94]
                            compl_payload                = data_payload 
                            data = [[ compl_fmt, compl_type, compl_t9, compl_tc, compl_t8, compl_attr1, compl_ln, compl_th, compl_td, compl_ep, compl_attr0, compl_at, compl_length, compl_completion_id ,compl_compl_status, compl_bcm, compl_byte_count, compl_requester_id, compl_tag, compl_reserved_r, compl_lower_address,compl_payload]]
                            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', 'compl_payload']
                            table = tabulate(data, headers=headers, tablefmt='orgtbl')
                            rc_to_ep_compl.write("{}\n".format(table))

                    def send_completion_failed_to_ep_tlp(ep_queue, data_payload):
                        #data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be,  str_completion_id ,str_rsv_10_7, str_ext_register_num, str_register_num, str_rsv_11_1]]
                        c_fmt                    = ep_queue[:3]

                        if(int(c_fmt[1], 2) == 1):
                            compl_fmt = format(0, '03b')				
                        else:
                            compl_fmt = format(2, '03b')
                        
                        compl_type                   = format(10,'05b')         #
                        if (compl_type[0:4] == '0000' and compl_fmt == '000') or (compl_type[2] == '1' and (compl_fmt in ['000','010'])): 
                            compl_t9                     = ep_queue[9]          #
                            compl_tc                     = ep_queue[9:12]       #
                            compl_t8                     = ep_queue[12]         #
                            compl_attr1                  = ep_queue[13]         #
                            compl_ln                     = ep_queue[14]         #
                            compl_th                     = ep_queue[15]         #
                            compl_td                     = ep_queue[16]         #
                            compl_ep                     = ep_queue[17]         #
                            compl_attr0                  = ep_queue[18:20]      #
                            compl_at                     = ep_queue[20:22]      #
                            compl_length                 = ep_queue[22:32]      #
                            compl_completion_id          = format(0x00ff,'016b')   
                            compl_compl_status           = format(1,'03b')
                            compl_bcm                    = format(0,'01b')      
                            compl_byte_count             = format(4,'012b')   
                            compl_requester_id           = ep_queue[32:48]  
                            compl_tag                    = ep_queue[48:56]   
                            compl_reserved_r             = format(0,'01b') 
                            read_addr                    = ep_queue[64:94]
                            compl_lower_address          = ep_queue[89:96]
                            compl_payload                = data_payload 
                            data = [[ compl_fmt, compl_type, compl_t9, compl_tc, compl_t8, compl_attr1, compl_ln, compl_th, compl_td, compl_ep, compl_attr0, compl_at, compl_length, compl_completion_id ,compl_compl_status, compl_bcm, compl_byte_count, compl_requester_id, compl_tag, compl_reserved_r, compl_lower_address,compl_payload]]
                            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', 'compl_payload']
                            table = tabulate(data, headers=headers, tablefmt='orgtbl')
                            rc_to_ep_compl.write("{}\n".format(table))
                        

                if str_type == '01010':
                    ## Recieving Completion from EP side
                    completion_recieved(ep_queue)
                elif str_type in ['00101' , '00000']:
                    ## Recieving TLP packets from EP side
                    #logger.info("----------------------RECIEVING  EP SIDE PACKETS AT RC SIDE ---------------------------")
                    ep_tx_recieved(ep_queue)
            packet_numbers +=1
            bin_f.close()
            ep_tx_bin_f.close()
        rc_mem_f.close()

#from pcie_rc_completion_rsp_ep_tx import *
           
            #for j in range(len(self.ep_err_pkt_no_arr_with_compl)):
            #    logger.info("error error entering arr_error")
            #    
            #    ep_err_arr_positive = [abs(num) for num in ep_err_arr]
          
# Sort i#n ascending order
        #    ep_err_arr_sorted = sorted(ep_err_arr_positive)
          
        #    if self.ep_err_pkt_no_arr_with_compl[j] == ep_err_arr_sorted[j]:
        #        rc_checker_f.write("injected packet from ep side MATCHES with detected error packet from RC checker side : EP injected pkt no : {} , RC detected error pke no : {}\n".format(str(self.ep_err_pkt_no_arr_with_compl[j],str(ep_err_arr_sorted[j]))))  
        #    else:
        #        rc_checker_f.write("injected packet from ep side MISMATCH with detected error packet from RC checker side : EP injected pkt no : {} , RC detected error pke no : {}\n".format(str(self.ep_err_pkt_no_arr_with_compl[j],str(ep_err_arr_sorted[j]))))  
        #        logger.warning("injected packet from ep side MISMATCH with detected error packet from RC checker side : EP injected pkt no : {} , RC detected error pke no : {}\n".format(str(self.ep_err_pkt_no_arr_with_compl[j],str(ep_err_arr_sorted[j]))))  


                 
                                                                
#check =e_rc_rx_ pkt_checker()                                  
#check.r_checker ()                                             
#rc_checf.close( )                                              
                                                                
                                                               
