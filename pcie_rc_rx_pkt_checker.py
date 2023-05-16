from pcie_com_file import compl_pkt_queue
#from pcie_seq_rc_config_pkt import *

print("hello ")
rc_checker_f = open("rc_checker_log.txt","w")
class pcie_rc_rx_pkt_checker:#(pcie_seq_rc_config_pkt):
    def rc_rx_checker(self):
        #num_pkts = argv.num_pkts
        for i in range(compl_pkt_queue.qsize()):
            ep_queue = compl_pkt_queue.queue[i]
            print(ep_queue)
 
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
            print(str_reserved_r) 
            str_lower_address          = ep_queue[89:96]
            print(str_lower_address          ) 

            print(
            str_fmt          ,           
            str_type        ,
            str_t9          ,
            str_tc          ,
            str_t8          ,
            str_attr1       ,
            str_ln          ,
            str_th          ,
            str_td          ,
            str_ep          ,
            str_attr0       ,
            str_at          ,
            str_length        , 
            str_completer_id  ,
            str_compl_status  ,
            str_bcm           ,
            str_byte_count    ,
            str_requester_id  ,
            str_tag           ,
            str_reserved_r    ,
            str_lower_address ,
             )

            print("str_completer_id is ",int(str_completer_id,2))
            print("str_completer_id is ",hex(int(str_completer_id,2)))
            rc_checker_f.write("-------------------------------------------------------------------------- TLP ")
            rc_checker_f.write(str(i))
            rc_checker_f.write(" ------------------------------------------------------------------------- ")
            rc_checker_f.write("\n")

            if int(str_fmt,2) in [0,2]:
                print("VALID fmt RECIEVED")
                if int(str_type        ,2) in [10]:
                    if int(str_t9,2) == 0:
                        if int(str_tc          ,2) == 0:
                            if int(str_t8,2) == 0:
                                if int(str_attr1       ,2) == 0:
                                    if int(str_ln,2) == 0:
                                        if int(str_th          ,2) == 0:
                                            if int(str_td          ,2) == 0:
                                                if int(str_ep          ,2) == 0:
                                                    if int(str_attr0       ,2) == 0:
                                                        if int(str_at          ,2) == 0:
                                                            if int(str_length      ,2) in range(2**10-1):
                                                                if int(str_completer_id        ,2) in range(0,2**16-1): 
                                                                    if int(str_compl_status                 ,2) in range(0,2**3-1):
                                                                        if int(str_bcm          ,2) == 0:
                                                                            if int(str_byte_count         ,2) in range(0,2**12-1):
                                                                                if (int(str_requester_id        ,2)>0 ):
                                                                                    if int(str_tag        ,2) in range(0,2**8-1):
                                                                                        #if int(str_ext_register_number ,2) == 0:
                                                                                            #if int(str_register_number     ,2) in range(0,2**6-1):
                                                                                        if int(str_reserved_r        ,2) == 0:
                                                                                            print("reserved_bit--------->",str_reserved_r)
                                                                                            if (int(str_lower_address             ,2)>0) in range(0,2**7-1):
                                                                                                rc_checker_f.write("Config Type 0 WRITE Request (CfgRd0) with 3DW, with data")
                                                                                                rc_checker_f.write("\n")
                                                                                                
                                                                                            elif (int(str_lower_address             ,2)==0) and int(str_fmt,2)==0:
                                                                                                rc_checker_f.write("Config Type 0 READ Request (CfgRd0) with 3DW, no data")
                                                                                                rc_checker_f.write("\n")

                                                                                            elif(int(str_lower_address             ,2)<0):
                                                                                                rc_checker_f.write("INVALID LOWER_ADDRESS RECIEVED: lower_address CANNOT BE NEGATIVE [Note : Please check and declare the lower_address with range 0 to (2**32)-1] ")
                                                                                                rc_checker_f.write("\n")

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


                                                                                        ## reserved_r else
                                                                                        else:
                                                                                            rc_checker_f.write("INVALID RESERVE_R RECIEVED: reserve_r CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of reserve_bit r as 0 (as it is unused)")
                                                                                            rc_checker_f.write("\n")

                                                                                    ## tag else
                                                                                    else:
                                                                                        rc_checker_f.write("INVALID TAG RECIEVED: tag CANNOT BE NEGATIVE or GREATER THAN 2**8-1 [Note : Please check and assign the value with in the range(0,2**8-1)")
                                                                                        rc_checker_f.write("\n")
                                                                                #completer_id else
                                                                                else:
                                                                                    rc_checker_f.write("INVALID REQUESTER_ID RECIEVED: requester_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)")
                                                                                    rc_checker_f.write("\n")
                                                                            #byte_count else
                                                                            else:
                                                                                rc_checker_f.write("INVALID BYTE_COUNT RECIEVED: byte_count CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**12-1)")
                                                                                rc_checker_f.write("\n")
                                                                        #last_dw_be else
                                                                        else:
                                                                            rc_checker_f.write("INVALID BCM RECIEVED: bcm CANNOT BE NEGATIVE or GREATER THAN 2**4-1 [Note : Please check and assign the value with in the range(0,2**4-1)")
                                                                            rc_checker_f.write("\n")
                                                                    #tag else
                                                                    else:
                                                                        rc_checker_f.write("INVALID COMPL_STATUS RECIEVED: compl_status CANNOT BE NEGATIVE or GREATER THAN 2**8-1 [Note : Please check and assign the value with in the range(0,2**8-1)")
                                                                        rc_checker_f.write("\n")
                                                                #completer_id else
                                                                else:
                                                                    rc_checker_f.write("INVALID COMPLETER_ID RECIEVED: completer_id CANNOT BE NEGATIVE or GREATER THAN 2**16-1 [Note : Please check and assign the value with in the range(0,2**16-1)")
                                                                    rc_checker_f.write("\n")
                                                            #length else
                                                            else:
                                                                rc_checker_f.write("INVALID LENGTH RECIEVED: length CANNOT BE NEGATIVE or GREATER THAN 2**10-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                                rc_checker_f.write("\n")
                                                        #at else
                                                        else:
                                                            rc_checker_f.write("INVALID AT RECIEVED: at CANNOT BE NEGATIVE or GREATER THAN 2**2-1 [Note : Please check and assign the value with in the range(0,2**10-1)")
                                                            rc_checker_f.write("\n")
                                                    #attr0 else
                                                    else:
                                                        rc_checker_f.write("INVALID ATTR0 RECIEVED: attr0 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                        rc_checker_f.write("\n")
                                                #ep else
                                                else:
                                                    rc_checker_f.write("INVALID EP RECIEVED: ep CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                    rc_checker_f.write("\n")
                                            #td else
                                            else:
                                                rc_checker_f.write("INVALID TD RECIEVED: td CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                                rc_checker_f.write("\n")
                                        #th else
                                        else:
                                            rc_checker_f.write("INVALID TH RECIEVED: th CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                            rc_checker_f.write("\n")
                                                                                    
                                    ## ln else
                                    else:
                                        rc_checker_f.write("INVALID LN RECIEVED: ln CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of ln as 0 (as it is unused)")
                                        rc_checker_f.write("\n")
                                ## attr1 else
                                else:
                                    rc_checker_f.write("INVALID ATTR1 RECIEVED: attr1 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value with in the range(0,1)")
                                    rc_checker_f.write("\n")

                            ## t8 else
                            else:
                                rc_checker_f.write("INVALID T8 RECIEVED: t8 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t8 as 0 (as it is unused)")
                                rc_checker_f.write("\n")
                        ## tc else
                        else:
                            rc_checker_f.write("INVALID TC RECIEVED: tc CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,7)")
                            rc_checker_f.write("\n")
                    ## t9 else
                    else:
                        rc_checker_f.write("INVALID T9 RECIEVED: t9 CANNOT BE NEGATIVE or GREATER THAN 1 [Note : Please check and assign the value of t9 as 0 (as it is unused)")
                        rc_checker_f.write("\n")
                ## type else
                else:
                    rc_checker_f.write("INVALID TYPE RECIEVED: type CANNOT BE NEGATIVE or GREATER THAN 31 [Note : Please check and assign the value with in the range(0,2**5-1)")
                    rc_checker_f.write("\n")
            ## fmt else
            else:
                rc_checker_f.write("INVALID FMT RECIEVED: fmt CANNOT BE NEGATIVE or GREATER THAN 2**3-1 [Note : Please check and assign the value with in the range(0,2**3-1)")
                rc_checker_f.write("\n")
                                    
            #if(int(str_completer_id,2)>0):
                #loggin.info("VALID completer_id RECIEVED")
            #    rc_checker_f.write("")
            #    rc_checker_f.write("\n")


            #elif(int(str_completer_id,2)<0):
            #    loggin.info("INVALID completer_id RECIEVED")

#check = pcie_rc_rx_pkt_checker()
#check.rc_rx_checker()
#
#rc_checker_f.close()


