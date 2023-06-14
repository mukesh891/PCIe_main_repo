from pcie_com_file import *
from pcie_rc_com_file import *
from tabulate import tabulate
from pcie_lib import *
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_rx_pkt_checker.py file")
logger.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_rx_pkt_checker.py file")
import queue
req_queue = queue.Queue()
tag_queue = queue.Queue()
# creating file for completion id check #
rc_checker_f = open("gen_logs/rc_checker_log.txt","w")

from pcie_rc_driver import rc_error_count_for_write_mem

#from pcie_ep_err_call_fn import ep_err_arr

class pcie_rc_rx_pkt_checker:#(pcie_seq_rc_config_pkt):
    def __init__(self):
        ep_err_eij_q =[]
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

        ep_tx_bin_f = open("gen_logs/ep_tx_recieved_bin.txt","w")
        ep_tx_bin_f.truncate(0)
        ep_tx_bin_f.close()

    def rc_rx_checker(self):
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
            #for i in range(compl_pkt_queue.qsize()):       
                # ep_queue is a string type -> reading data from compl_queue #
                #ep_queue = compl_pkt_queue.queue[i] 
                # assgning all filed value from ep_queue #
                str_fmt                    = ep_queue[:3]         #
                str_type                   = ep_queue[3:8]        #
                str_t9                     = ep_queue[9]          #
                str_tc                     = ep_queue[9:12]       #
                str_t8                     = ep_queue[13]         #
                str_attr1                  = ep_queue[14]         #
                str_ln                     = ep_queue[15]         #
                str_th                     = ep_queue[16]         #
                str_td                     = ep_queue[17]         #
                str_ep                     = ep_queue[18]         #
                str_attr0                  = ep_queue[18:20]      #
                str_at                     = ep_queue[20:22]      #
                str_length                 = ep_queue[22:32]      #
                
                
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
                        str_payload = ep_queue[96:]                    
                                                                       
                        # printing header for rc_checker_log.txt file #
                        rc_checker_f.write("-------------------------------------------------------------------------- TLP ")
                        rc_checker_f.write(str(packet_numbers))
                        rc_checker_f.write(" ------------------------------------------------------------------------- ")
                        rc_checker_f.write("\n")
                        rc_checker_f.write('\nCompletion packet recieved -> {}\n'.format(ep_queue))
                        
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
                                                                                                        rc_checker_f.write("INVALID RESERVE_R RECIEVED: reserved_r CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of reserve_bit r as 0 (as it is unused), VALUE RECIEVED : {}".format(int(str_reserved_r,2)))
                                                                                                        rc_checker_f.write("\n")
                                                                                                        rc_checker_f.write("\n")
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.compl_err_pkts.append(self.iteration)
                 
                                                                                                ## tag else
                                                                                                else:
                                                                                                    rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 2**8-1 [Note : Please check and assign the value with in the range(0,2**8-1), VALUE RECIEVED : {}".format(int(str_tag,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("\n")
                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                    self.compl_err_pkts.append(self.iteration)
                                                                                            #completer_id else
                                                                                            else:
                                                                                                rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1), VALUE RECIEVED : {}".format(int(str_requester_id,2)))
                                                                                                rc_checker_f.write("\n")
                                                                                                rc_checker_f.write("\n")
                                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                self.compl_err_pkts.append(self.iteration)
                                                                                        #byte_count else
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID BYTE_COUNT RECIEVED: byte_count CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**12-1), VALUE RECIEVED : {}".format(int(str_byte_count,2)))
                                                                                            rc_checker_f.write("\n")
                                                                                            rc_checker_f.write("\n")
                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                            self.compl_err_pkts.append(self.iteration)
                                                                                    #last_dw_be else
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID BCM RECIEVED: bcm CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**4-1), VALUE RECIEVED : {}".format(int(str_bcm,2)))                                                                               
                                                                                        rc_checker_f.write("\n")
                                                                                        rc_checker_f.write("\n")
                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                        self.compl_err_pkts.append(self.iteration)
                                                                                #tag else
                                                                                else:
                                                                                    rc_checker_f.write("INVALID COMPL_STATUS RECIEVED: compl_status CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,2**8-1), VALUE RECIEVED : {}".format(int(str_compl_status,2)))
                                                                                    rc_checker_f.write("\n")
                                                                                    rc_checker_f.write("\n")
                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                    self.compl_err_pkts.append(self.iteration)
                                                                            #completer_id else
                                                                            else:
                                                                                rc_checker_f.write("INVALID COMPLETER_ID RECIEVED: completion_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1), VALUE RECIEVED : {}".format(int(str_completion_id,2)))
                                                                                rc_checker_f.write("\n")
                                                                                rc_checker_f.write("\n")
                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                self.compl_err_pkts.append(self.iteration)
                                                                        #length else
                                                                        else:
                                                                            rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 2**10-1 [Note : Please check and assign the value with in the range(0,2**10-1), VALUE RECIEVED : {}".format(int(str_length,2)))
                                                                            rc_checker_f.write("\n")
                                                                            rc_checker_f.write("\n")
                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                            self.compl_err_pkts.append(self.iteration)
                                                                    #at else
                                                                    else:
                                                                        rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 2**2-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                                        rc_checker_f.write("\n")
                                                                        rc_checker_f.write("\n")
                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                        self.compl_err_pkts.append(self.iteration)
                                                                #attr0 else
                                                                else:
                                                                    rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}".format(int(str_at,2)))
                                                                    rc_checker_f.write("\n")
                                                                    rc_checker_f.write("\n")
                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                    self.compl_err_pkts.append(self.iteration)
                                                            #ep else
                                                            else:
                                                                rc_checker_f.write("INVALID EP RECIEVED: ep CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}".format(int(str_ep,2)))
                                                                rc_checker_f.write("\n")
                                                                rc_checker_f.write("\n")
                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                self.compl_err_pkts.append(self.iteration)
                                                        #td else
                                                        else:
                                                            rc_checker_f.write("INVALID TD RECIEVED: td CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}".format(int(str_td,2)))
                                                            rc_checker_f.write("\n")
                                                            rc_checker_f.write("\n")
                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                            self.compl_err_pkts.append(self.iteration)
                                                    #th else
                                                    else:
                                                        rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}".format(int(str_th,2)))
                                                        rc_checker_f.write("\n")
                                                        rc_checker_f.write("\n")
                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                        self.compl_err_pkts.append(self.iteration)
                                                                                                
                                                ## ln else
                                                else:
                                                    rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of ln as 0 (as it is unused), VALUE RECIEVED : {}".format(int(str_type,2)))
                                                    rc_checker_f.write("\n")
                                                    rc_checker_f.write("\n")
                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                    self.compl_err_pkts.append(self.iteration)
                                            ## attr1 else
                                            else:
                                                rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1), VALUE RECIEVED : {}".format(int(str_ln,2)))
                                                rc_checker_f.write("\n")
                                                rc_checker_f.write("\n")
                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                self.compl_err_pkts.append(self.iteration)
                 
                                        ## t8 else
                                        else:
                                            rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t8 as 0 (as it is unused), VALUE RECIEVED : {}".format(int(str_t8,2)))
                                            rc_checker_f.write("\n")
                                            rc_checker_f.write("\n")
                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                            self.compl_err_pkts.append(self.iteration)
                                    ## tc else
                                    else:
                                        rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,7), VALUE RECIEVED : {}".format(int(str_tc,2)))
                                        rc_checker_f.write("\n")
                                        rc_checker_f.write("\n")
                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                        self.compl_err_pkts.append(self.iteration)
                                ## t9 else
                                else:
                                    rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t9 as 0 (as it is unused), VALUE RECIEVED : {}".format(int(str_t9,2)))
                                    rc_checker_f.write("\n")
                                    rc_checker_f.write("\n")
                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                    self.compl_err_pkts.append(self.iteration)
                            ## type else
                            else:
                                rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 31 [Note : Please check and assign the value with in the range(0,2**5-1), VALUE RECIEVED : {}".format(int(str_type,2)))
                                rc_checker_f.write("\n")
                                rc_checker_f.write("\n")
                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                self.compl_err_pkts.append(self.iteration)
                        ## fmt else
                        else:
                            rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,2**3-1), VALUE RECIEVED : {}".format(int(str_fmt,2)))
                            rc_checker_f.write(str_fmt)
                            rc_checker_f.write(line[0:3])
                            rc_checker_f.write("\n")
                            rc_checker_f.write("\n")
                            self.bad_pkts=self.bad_pkts+1                                                                                                
                            self.compl_err_pkts.append(self.iteration)
                 
                        
                        data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_completion_id ,str_compl_status, str_bcm, str_byte_count, str_requester_id, str_tag, str_reserved_r, str_lower_address]]
                        headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', '']
                        table = tabulate(data, headers=headers, tablefmt='orgtbl')
                        rc_checker_f.write(table) 
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n") 
                        rc_checker_f.write("\n")                    
                        rc_checker_f.write("GOOD_PKTS RECIEVED =")
                        rc_checker_f.write(str(self.good_pkts))
                        rc_checker_f.write("\n")
                        rc_checker_f.write("BAD_PKT RECIEVED =")
                        rc_checker_f.write(str(self.bad_pkts))
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n")
                 
                def ep_tx_recieved(ep_queue):

                    if str_type in ['00101' , '00000']:
                        ep_tx_bin_f.write("{}\n".format(ep_queue))
                 
                        rc_checker_f.write("-------------------------------------------------------------------------- TLP ")
                        rc_checker_f.write(str(packet_numbers))
                        rc_checker_f.write(" ------------------------------------------------------------------------- ")
                        rc_checker_f.write("\n")
                        rc_checker_f.write('\nEP generated packet recieved -> {}\n'.format(ep_queue))
                        str_requester_id = ep_queue[32:48]             
                        str_tag = ep_queue[48:56]                      
                        str_last_dw_be = ep_queue[56:60]                   
                        str_first_dw_be = ep_queue[60:64]                  
                                                                       
                        if (str_type[2] == '1'):            #          
                            str_completion_id = ep_queue[64:80]           
                            str_rsv_10_7 = ep_queue[80:84]       #        
                            str_ext_register_num = ep_queue[84:88]        
                            str_register_num = ep_queue[88:94]            
                            str_rsv_11_1 = ep_queue[94:96]       #        
                            str_payload= ep_queue[96:len(ep_queue)-32]       #        
                            str_ecrc = ep_queue[len(ep_queue)-32:]       #        
                        elif(str_type[0:4] == '0000'):      #             
                            str_address = ep_queue[64:94]                 
                            str_rsv_11_1 = ep_queue[94:96]                 
                            str_payload= ep_queue[96:len(ep_queue)-32]       #        
                            str_ecrc = ep_queue[len(ep_queue)-32:]       #        
                 
                        if(len(str_payload)%32 == 0):
                            pass
                        else:
                            logger.error("PAYLOAD SIZE IS UNALLIGNED, LENGTH OF PAYLOAD IS : {}".format(len(str_payload)))
                 
                 
                 
                        tlp_packet_without_ecrc  = ep_queue[:len(ep_queue)-32]
                        integer_tlp_value = int(tlp_packet_without_ecrc , 2)
                        ecrc_divisor = int(fixed_ecrc_divisor, 2)
                        integer_ecrc_value = integer_tlp_value % ecrc_divisor 
                        #remainder = integer_value % fixed_integer_value
                        ecrc_value = bin(integer_ecrc_value)[2:].zfill(32)
                        print("----------------->",str_ecrc, ecrc_value)
                        if(ecrc_value == str_ecrc):
                            logger.info("EP ecrc value MISMATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(ep_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                            rc_checker_f.write("EP ecrc value MATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(ep_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                        else:
                            rc_checker_f.write("EP ecrc value MISMATCHES with calculated ecrc value : Recieved pkt : {} \n EP ECRC : {} , CALCULATED ECRC : {} \n".format(ep_queue,int(ecrc_value,2) , int(str_ecrc,2)))
                            #logger.error("EP ecrc value MISMATCHES with calculated ecrc value : EP ECRC : {} , CALCULATED ECRC : {} \n".format(int(ecrc_value,2) , int(str_ecrc,2)))
                            
                        
                        ##
                        if (str_fmt[0:3] in ['010','000']): 
                            #print("VALID fmt RECIEVED")
                            if int(str_type        ,2) in [0,5]:
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
                                                        if int(str_td          ,2) == 0:                # ep completer: td will be 0
                                                            if int(str_ep          ,2) == 0:            # ep completer: ep must be 0
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
                                                                                                                    ep_err_eij_q.append(self.ep_pkts_iter)
                                                                                                                    #data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be,  str_completion_id ,str_rsv_10_7, str_ext_register_num, str_register_num, str_rsv_11_1]]
                                                                                                                    #headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Requester_Id', 'Tag', ' last_dw_be' ,'first_dw_be', 'Completion_Id', 'rsv_10_7','ext_register_num', 'str_register_num', 'str_rsv_11_1','']
                                                                                                                    #table = tabulate(data, headers=headers, tablefmt='orgtbl')
                 
                                                                                                                else:
                                                                                                                    rc_checker_f.write("INVALID str_rsv_11_1 RECIEVED: rsv_11_1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_rsv_11_1,2)))
                                                                                                                    rc_checker_f.write("\n")
                                                                                                                    rc_checker_f.write("\n")
                                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                            else:
                                                                                                                rc_checker_f.write("INVALID REGISTER_NUMBER RECIEVED: register_num CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_register_num,2)))
                                                                                                                rc_checker_f.write("\n")
                                                                                                                rc_checker_f.write("\n")
                                                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                        else:
                                                                                                            rc_checker_f.write("INVALID EXT_REGISTER_NUMBER RECIEVED: ext_register_num CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_ext_register_num,2)))
                                                                                                            rc_checker_f.write("\n")
                                                                                                            rc_checker_f.write("\n")
                                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                    else:
                                                                                                        rc_checker_f.write("INVALID rsv_10_7 RECIEVED: rsv_10_7 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_rsv_10_7,2)))
                                                                                                        rc_checker_f.write("\n")
                                                                                                        rc_checker_f.write("\n")
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                else:
                                                                                                    rc_checker_f.write("INVALID COMPLETION_ID RECIEVED: completion_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)] VALUE RECIEVED : {}".format(int(str_completion_id,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("\n")
                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                                    
                                                                                            elif(str_type[0:4] == '0000'):
                                                                                                if int(str_address      ,2) < 2**30 :                                # ep completer: length will be 1
                                                                                                    if int(str_rsv_11_1      ,2) == 0  :                                # ep completer: length will be 1
                                                                                                        self.good_pkts = self.good_pkts + 1
                                                                                                        self.ep_gen_good_pkts=self.ep_gen_good_pkts+1                                                                                                
                                                                                                    # else :str_rsv_11_1      
                                                                                                    else:
                                                                                                        rc_checker_f.write("INVALID rsv_11_1 RECIEVED: rsv_11_1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_rsv_11_1,2)))
                                                                                                        rc_checker_f.write("\n")
                                                                                                        rc_checker_f.write("\n")
                                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                                # else :str_address      
                                                                                                else:
                                                                                                    rc_checker_f.write("INVALID ADDRESS RECIEVED: address CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_address,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("\n")
                                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                        # else :str_first_dw_be
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID FIRST_DW_BE RECIEVED: first_dw_be CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_first_dw_be,2)))
                                                                                            rc_checker_f.write("\n")
                                                                                            rc_checker_f.write("\n")
                                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                    # else :str_last_dw_be
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID LAST_DW_BE RECIEVED: last_dw_be CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_last_dw_be,2)))
                                                                                        rc_checker_f.write("\n")
                                                                                        rc_checker_f.write("\n")
                                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                                # else :str_tag
                                                                                else:
                                                                                    rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_tag,2)))
                                                                                    rc_checker_f.write("\n")
                                                                                    rc_checker_f.write("\n")
                                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                            # else :str_requester_id
                                                                            else:
                                                                                rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_requester_id,2)))
                                                                                rc_checker_f.write("\n")
                                                                                rc_checker_f.write("\n")
                                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                        # else :str_length
                                                                        else:
                                                                            rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_length,2)))
                                                                            rc_checker_f.write("\n")
                                                                            rc_checker_f.write("\n")
                                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                    # else :str_at
                                                                    else:
                                                                        rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_at,2)))
                                                                        rc_checker_f.write("\n")
                                                                        rc_checker_f.write("\n")
                                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                                # else :str_attr0
                                                                else:
                                                                    rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_attr0,2)))
                                                                    rc_checker_f.write("\n")
                                                                    rc_checker_f.write("\n")
                                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                            # else :str_ep
                                                            else:
                                                                rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_ep,2)))
                                                                rc_checker_f.write("\n")
                                                                rc_checker_f.write("\n")
                                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                        # else :str_td
                                                        else:
                                                            rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_ln,2)))
                                                            rc_checker_f.write("\n")
                                                            rc_checker_f.write("\n")
                                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                    # else :str_th
                                                    else:
                                                        rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_th,2)))
                                                        rc_checker_f.write("\n")
                                                        rc_checker_f.write("\n")
                                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                                # else :str_ln
                                                else:
                                                    rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_ln,2)))
                                                    rc_checker_f.write("\n")
                                                    rc_checker_f.write("\n")
                                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                            # else :str_attr1
                                            else:
                                                rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_attr1,2)))
                                                rc_checker_f.write("\n")
                                                rc_checker_f.write("\n")
                                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                        # else :str_t8
                                        else:
                                            rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_t8,2)))
                                            rc_checker_f.write("\n")
                                            rc_checker_f.write("\n")
                                            self.bad_pkts=self.bad_pkts+1                                                                                                
                                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                    # else :str_tc
                                    else:
                                        rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 7 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}".format(int(str_tc,2)))
                                        rc_checker_f.write("\n")
                                        rc_checker_f.write("\n")
                                        self.bad_pkts=self.bad_pkts+1                                                                                                
                                        self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                        self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                        self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                                # else :str_t9
                                else:
                                    rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)] VALUE RECIEVED : {}".format(int(str_t9,2)))
                                    rc_checker_f.write("\n")
                                    rc_checker_f.write("\n")
                                    self.bad_pkts=self.bad_pkts+1                                                                                                
                                    self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                    self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                    self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                            # else :str_type
                            else:                                                                                    
                                rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 15 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}".format(int(str_type,2)))
                                rc_checker_f.write("\n")
                                rc_checker_f.write("\n")
                                self.bad_pkts=self.bad_pkts+1                                                                                                
                                rc_checker_f.write("\n") 
                                self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                                self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                                self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                        # else :str_fmt
                        else:
                            rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 7 [Note : Please check and assign the value with in the range(0,2**3-1)] VALUE RECIEVED : {}".format(int(str_type,2)))
                            rc_checker_f.write("\n")
                            rc_checker_f.write("\n")
                            self.bad_pkts=self.bad_pkts+1                                                                                                
                            self.ep_gen_bad_pkts=self.ep_gen_bad_pkts+1                                                                                                
                            self.ep_err_pkt_no_arr.append(self.ep_pkts_iter)
                            self.ep_err_pkt_no_arr_with_compl.append(self.iteration)       
                 
                                                                                                                 
                 
                 
                        
                        if (str_type[2] == '1'):                      
                            data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be,  str_completion_id ,str_rsv_10_7, str_ext_register_num, str_register_num, str_rsv_11_1]]
                            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Requester_Id', 'Tag', ' last_dw_be' ,'first_dw_be', 'Completion_Id', 'rsv_10_7','ext_register_num', 'str_register_num', 'str_rsv_11_1','']
                            table = tabulate(data, headers=headers, tablefmt='orgtbl')
                            rc_checker_f.write(table) 
                 
                        elif(str_type[0:4] == '0000'):                   
                            data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_requester_id,str_tag,str_last_dw_be,str_first_dw_be, str_address, str_rsv_11_1]]
                            headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Requester_Id', 'Tag', ' last_dw_be' ,'first_dw_be', 'str_address', 'str_rsv_11_1', '']
                            table = tabulate(data, headers=headers, tablefmt='orgtbl')
                            rc_checker_f.write(table) 
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n") 
                        rc_checker_f.write("\n")                    
                        rc_checker_f.write("GOOD_PKTS RECIEVED = {}\n".format(str(self.good_pkts)))
                        rc_checker_f.write("BAD_PKT RECIEVED = {}\n".format(str(self.bad_pkts)))
                        rc_checker_f.write("self.ep_cfg_read_req_pkts_rcvd = {}\n".format(str(self.ep_cfg_read_req_pkts_rcvd)))
                        rc_checker_f.write("self.ep_cfg_write_req_pkts_rcvd = {}\n".format(str(self.ep_cfg_write_req_pkts_rcvd)))
                        rc_checker_f.write("self.ep_mem_read_req_rcvd = {}\n".format(str(self.ep_mem_read_req_rcvd)))
                        rc_checker_f.write("self.ep_mem_write_req_rcvd = {}\n".format(str(self.ep_mem_write_req_rcvd)))
                        rc_checker_f.write("total good packets from EP generator side = {}\n".format(str(self.ep_gen_good_pkts)))
                        rc_checker_f.write("total error/bad packets from EP generator side = {}\n".format(str(self.ep_gen_bad_pkts)))
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n")
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
                    rc_checker_f.write("EP error injected pkts with completion packets : {}\n".format(str(self.ep_err_pkt_no_arr_with_compl)))  
                     
                    self.iteration += 1
                    __all__ = ['self.ep_err_pkt_no_arr']
                
                    #def send_completion_to_ep_tlp(ep_queue):



                if str_type == '01010':
                    ## Recieving Completion from EP side
                    completion_recieved(ep_queue)
                elif str_type in ['00101' , '00000']:
                    ## Recieving TLP packets from EP side
                    ep_tx_recieved(ep_queue)
            packet_numbers +=1
            bin_f.close()
            ep_tx_bin_f.close()

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
                                                                
                                                               
