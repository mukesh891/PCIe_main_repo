from pcie_com_file import compl_pkt_queue
#from pcie_seq_rc_config_pkt import *
from tabulate import tabulate
print("hello ")
# creating file for completion id check #
rc_checker_f = open("gen_logs/rc_checker_log.txt","w")
bin_f = open("gen_logs/rc_mem_bin_file.txt","r")
class pcie_rc_rx_pkt_checker:#(pcie_seq_rc_config_pkt):
    def rc_rx_checker(self):
        #num_pkts = argv.num_pkts
        # loop for reading values from compl_pkt_queue #
        #for i in range(compl_pkt_queue.qsize()):
        i=0
        good_pkts = 0
        bad_pkts =0
        for line in bin_f: 
            if i < compl_pkt_queue.qsize():            
                # ep_queue is a string type -> reading data from compl_queue #
                ep_queue = compl_pkt_queue.queue[i] 
                # assgning all filed value from ep_queue #
                str_fmt                    = ep_queue[:3]
                str_type                   = ep_queue[3:8]
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
                str_completer_id           = ep_queue[32:48]
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
                rc_checker_f.write(str(i))
                rc_checker_f.write(" ------------------------------------------------------------------------- ")
                rc_checker_f.write("\n")
                i=i+1
                
                # Checking all the completer fields for validation and range format #
                if ((line[0:3] == '000' and str_fmt[0:3] == '010') or ((line[0:3]) == '010' and str_fmt[0:3] == '000')): # ep completer: fmt will be 0 or 2
                    #print("VALID fmt RECIEVED")
                    if int(str_type        ,2) in [10]:         # ep completer: will be 10
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
                                                                    if int(str_completer_id        ,2) in range(0,2**16-1):    # ep completer: commpleter id must be greater than 0
                                                                        if int(str_compl_status                 ,2) == 0:      # ep completer: completer status must be 1 for pass adn 0 for fail packet
                                                                            if int(str_bcm          ,2) == 0:                  # ep completer: bcm will be 0
                                                                                if int(str_byte_count         ,2) in range(0,2**12-1):       # ep completer: byte_count must be within range 0 to 2**12-1
                                                                                    if (int(str_requester_id,2)  == int(line[32:48],2)):     # ep completer: requester_id must be same as generated requester id
                                                                                        if str_tag == line[48:56]:                   # ep completer: tag will be within range 0 to 2**8-1
                                                                                            if int(str_reserved_r,2) == 0:           # ep completer: reserved_bit will be 0 
                                                                                                #print("reserved_bit--------->",str_reserved_r)
                                                                                                if (int(str_lower_address             ,2)>0) in range(0,2**7-1): # ep completer: lower_address will be within 0 to 2**7-1

                                                                                                    rc_checker_f.write("fmt = ")
                                                                                                    rc_checker_f.write(hex(int(str_fmt,2))) 
                                                                                                    rc_checker_f.write("\n")                        
                                                                                                    rc_checker_f.write("type = ")
                                                                                                    rc_checker_f.write(hex(int(str_type,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("t9 = ")
                                                                                                    rc_checker_f.write(hex(int(str_t9,2)))       
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("tc = ")
                                                                                                    rc_checker_f.write(hex(int(str_tc,2       )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("t8 = ")
                                                                                                    rc_checker_f.write(hex(int(str_t8,2)))       
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("attr1 = ")
                                                                                                    rc_checker_f.write(hex(int(str_attr1,2       )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("ln = ")
                                                                                                    rc_checker_f.write(hex(int(str_ln,2)))      
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("th = ")  
                                                                                                    rc_checker_f.write(hex(int(str_th,2          )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("td = ")  
                                                                                                    rc_checker_f.write(hex(int(str_td,2          )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("ep = ") 
                                                                                                    rc_checker_f.write(hex(int(str_ep,2          )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("attr0 = ")
                                                                                                    rc_checker_f.write(hex(int(str_attr0,2       )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("at = ")
                                                                                                    rc_checker_f.write(hex(int(str_at,2          )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("length = ")
                                                                                                    rc_checker_f.write(hex(int(str_length,2      )))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("completer_id = ")
                                                                                                    rc_checker_f.write(hex(int(str_completer_id,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("compl_status = ")
                                                                                                    rc_checker_f.write(hex(int(str_compl_status,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("bcm = ")
                                                                                                    rc_checker_f.write(hex(int(str_bcm,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("byte_count = ")
                                                                                                    rc_checker_f.write(hex(int(str_byte_count,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("requester_id = ")
                                                                                                    rc_checker_f.write(hex(int(str_requester_id,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("tag = ")
                                                                                                    rc_checker_f.write(hex(int(str_tag,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write("lower_address = ")
                                                                                                    rc_checker_f.write(hex(int(str_lower_address,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    rc_checker_f.write(hex(int(str_payload,2)))
                                                                                                    rc_checker_f.write("\n")
                                                                                                    good_pkts=good_pkts+1
                                                                                                    
                                                                                                else:
                                                                                                    rc_checker_f.write("INVALID LOWER_ADDRESS RECIEVED: lower_address CANNOT BE NEGATIVE [Note : Please check and declare the value")


                                                                                            # reserved_r else
                                                                                            else:
                                                                                                rc_checker_f.write("INVALID RESERVE_R RECIEVED: reserve_r CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of reserve_bit r as 0 (as it is unused)")
                                                                                                rc_checker_f.write("\n")
                                                                                                rc_checker_f.write("\n")
                                                                                                bad_pkts=bad_pkts+1                                                                                                

                                                                                        ## tag else
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 2**8-1 [Note : Please check and assign the value with in the range(0,2**8-1)")
                                                                                            rc_checker_f.write("\n")
                                                                                            rc_checker_f.write("\n")
                                                                                            bad_pkts=bad_pkts+1                                                                                                
                                                                                    #completer_id else
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)")
                                                                                        rc_checker_f.write("\n")
                                                                                        rc_checker_f.write("\n")
                                                                                        bad_pkts=bad_pkts+1                                                                                                
                                                                                #byte_count else
                                                                                else:
                                                                                    rc_checker_f.write("INVALID BYTE_COUNT RECIEVED: byte_count CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**12-1)")
                                                                                    rc_checker_f.write("\n")
                                                                                    rc_checker_f.write("\n")
                                                                                    bad_pkts=bad_pkts+1                                                                                                
                                                                            #last_dw_be else
                                                                            else:
                                                                                rc_checker_f.write("INVALID BCM RECIEVED: bcm CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**4-1)")
                                                                                rc_checker_f.write("\n")
                                                                                rc_checker_f.write("\n")
                                                                                bad_pkts=bad_pkts+1                                                                                                
                                                                        #tag else
                                                                        else:
                                                                            rc_checker_f.write("INVALID COMPL_STATUS RECIEVED: compl_status CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,2**8-1)")
                                                                            rc_checker_f.write("\n")
                                                                            rc_checker_f.write("\n")
                                                                            bad_pkts=bad_pkts+1                                                                                                
                                                                    #completer_id else
                                                                    else:
                                                                        rc_checker_f.write("INVALID COMPLETER_ID RECIEVED: completer_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)")
                                                                        rc_checker_f.write("\n")
                                                                        rc_checker_f.write("\n")
                                                                        bad_pkts=bad_pkts+1                                                                                                
                                                                #length else
                                                                else:
                                                                    rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 2**10-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                                    rc_checker_f.write("\n")
                                                                    rc_checker_f.write("\n")
                                                                    bad_pkts=bad_pkts+1                                                                                                
                                                            #at else
                                                            else:
                                                                rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 2**2-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                                rc_checker_f.write("\n")
                                                                rc_checker_f.write("\n")
                                                                bad_pkts=bad_pkts+1                                                                                                
                                                        #attr0 else
                                                        else:
                                                            rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                            rc_checker_f.write("\n")
                                                            rc_checker_f.write("\n")
                                                            bad_pkts=bad_pkts+1                                                                                                
                                                    #ep else
                                                    else:
                                                        rc_checker_f.write("INVALID EP RECIEVED: ep CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                        rc_checker_f.write("\n")
                                                        rc_checker_f.write("\n")
                                                        bad_pkts=bad_pkts+1                                                                                                
                                                #td else
                                                else:
                                                    rc_checker_f.write("INVALID TD RECIEVED: td CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                    rc_checker_f.write("\n")
                                                    rc_checker_f.write("\n")
                                                    bad_pkts=bad_pkts+1                                                                                                
                                            #th else
                                            else:
                                                rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                rc_checker_f.write("\n")
                                                rc_checker_f.write("\n")
                                                bad_pkts=bad_pkts+1                                                                                                
                                                                                        
                                        ## ln else
                                        else:
                                            rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of ln as 0 (as it is unused)")
                                            rc_checker_f.write("\n")
                                            rc_checker_f.write("\n")
                                            bad_pkts=bad_pkts+1                                                                                                
                                    ## attr1 else
                                    else:
                                        rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                        rc_checker_f.write("\n")
                                        rc_checker_f.write("\n")
                                        bad_pkts=bad_pkts+1                                                                                                

                                ## t8 else
                                else:
                                    rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t8 as 0 (as it is unused)")
                                    rc_checker_f.write("\n")
                                    rc_checker_f.write("\n")
                                    bad_pkts=bad_pkts+1                                                                                                
                            ## tc else
                            else:
                                rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,7)")
                                rc_checker_f.write("\n")
                                rc_checker_f.write("\n")
                                bad_pkts=bad_pkts+1                                                                                                
                        ## t9 else
                        else:
                            rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t9 as 0 (as it is unused)")
                            rc_checker_f.write("\n")
                            rc_checker_f.write("\n")
                            bad_pkts=bad_pkts+1                                                                                                
                    ## type else
                    else:
                        rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 31 [Note : Please check and assign the value with in the range(0,2**5-1)")
                        rc_checker_f.write("\n")
                        rc_checker_f.write("\n")
                        bad_pkts=bad_pkts+1                                                                                                
                ## fmt else
                else:
                    rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,2**3-1), RECIEVED FMT value is :")
                    rc_checker_f.write(str_fmt)
                    rc_checker_f.write(line[0:3])
                    rc_checker_f.write("\n")
                    rc_checker_f.write("\n")
                    bad_pkts=bad_pkts+1                                                                                                
                data = [[ str_fmt, str_type, str_t9, str_tc, str_t8, str_attr1, str_ln, str_th, str_td, str_ep, str_attr0, str_at, str_length, str_completer_id ,str_compl_status, str_bcm, str_byte_count, str_requester_id, str_tag, str_reserved_r, str_lower_address]]
                headers = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', '']
                table = tabulate(data, headers=headers, tablefmt='orgtbl')
                rc_checker_f.write(table) 
                rc_checker_f.write("\n")
                rc_checker_f.write("\n") 
                rc_checker_f.write("\n")                    
                rc_checker_f.write("GOOD_PKTS RECIEVED =")
                rc_checker_f.write(str(good_pkts))
                rc_checker_f.write("\n")
                rc_checker_f.write("BAD_PKT RECIEVED =")
                rc_checker_f.write(str(bad_pkts))
                rc_checker_f.write("\n")
                rc_checker_f.write("\n")
                rc_checker_f.write("\n")


#check = pcie_rc_rx_pkt_checker()
#check.rc_rx_checker()
#rc_checker_f.close()
