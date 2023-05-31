from pcie_lib import *
#from pcie_com_file import *
from err_id_creation import *
from pcie_rc_generated_logs import *

#from pcie_rc_config_pkt import *
from pcie_rc_base_test import *

logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_driver.py file")

from pcie_rc_callback import *
err_id_f = open("gen_logs/error_id_file.txt","w") 
bin_f = open("gen_logs/rc_tx_good_bin_file.txt","r") 
err_bin_f = open("gen_logs/rc_tx_mixed_bin_file.txt","w")
class pcie_rc_driver:
    def __init__(self):
        self.k=0
        self.m=0
    def drive_tx(self):
        num_pkts= argv.num_pkts
        ln = ""
        ## INFO :Erro injection using commandline arg "--err_eij=1" ##
        for line in bin_f:
            line = line.strip('\n')
            # error injection enable
            if(err_eij):
                # m is no. of iterations till num_pkts-1
                # checking whether m is lessthan the no. of error pkts injected
                if(self.m < num_pkts):
                    # err_id_q is an array with size of err_pkt_no, You can get "err_pkt_no" and err_id_q in pcie_com_file.py
                    err_eij_hdl = pcie_err_eij()
                    if self.m in arr:
                        #print("m in arr",self.m)
                        ## randomly choose between bdf and fmt and type error
                        j = random.choice([3])
                        # If j==1 , then "fmt" will be injected with error 
                        if(j==0):
                            fmt = err_eij_hdl.pcie_fmt_err_eij()
                            fmt_str                 =format(fmt, '03b')       
                            #print("modified fmt->",fmt_str) 
                            ln =fmt_str+line[3:]
                            err_id_f.write("FMT_ERROR_")
                            err_id_f.write(fmt_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                            
                        # If j==0 , then "type" will be injected with error
                        if(j==1):
                            typ =err_eij_hdl.pcie_type_err_eij()
                            type_str=format(typ, '05b')       
                            #print(type_str) 
                            ln = line[:3]+type_str+line[8:] 
                            err_id_f.write("TYPE_ERROR_")
                            err_id_f.write(type_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==3):
                            TC =err_eij_hdl.pcie_TC_err_eij()
                            TC_str=format(TC, '03b')       
                            #print(TC_str) 
                            ln = line[:9]+TC_str+line[12:] 
                            err_id_f.write("TC_ERROR_")
                            err_id_f.write(TC_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==4):
                            Attr1 =err_eij_hdl.pcie_attr1_err_eij()
                            Attr1_str=format(Attr1, '01b')       
                            #print(Attr1_str) 
                            ln = line[:13]+Attr1_str+line[14:] 
                            err_id_f.write("Attr1_ERROR_")
                            err_id_f.write(Attr1_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==5):
                            TH =err_eij_hdl.pcie_TH_err_eij()
                            TH_str=format(TH, '01b')       
                            #print(TH_str)
                            #ln = TH_str+line[:15]
                            ln = line[:15]+TH_str+line[16:] 
                            err_id_f.write("TH_ERROR_")
                            err_id_f.write(TH_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==6):
                            TD =err_eij_hdl.pcie_TD_err_eij()
                            TD_str=format(Td, '01b')       
                            #print(TH_str)
                            #ln = TH_str+line[:15]
                            ln = line[:16]+TD_str+line[17:]
                            err_id_f.write("TD_ERROR_")
                            err_id_f.write(TD_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==7):
                            EP =err_eij_hdl.pcie_EP_err_eij()
                            EP_str=format(EP, '01b')       
                            #print(EP_str) 
                            ln = line[:17]+EP_str+line[18:] 
                            err_id_f.write("EP_ERROR_")
                            err_id_f.write(EP_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==8):
                            attr0 =err_eij_hdl.pcie_attr0_err_eij()
                            attr0_str=format(attr0, '02b')       
                            #print(attr0_str) 
                            ln = line[:18]+attr0_str+line[20:] 
                            err_id_f.write("attr0_ERROR_")
                            err_id_f.write(attr0_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==9):
                            AT =err_eij_hdl.pcie_AT_err_eij()
                            AT_str=format(AT, '02b')       
                            #print(AT_str) 
                            ln = line[:20]+AT_str+line[22:] 
                            err_id_f.write("AT_ERROR_")
                            err_id_f.write(AT_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==10):
                            length =err_eij_hdl.pcie_length_err_eij()
                            length_str=format(length, '10b')       
                            #print(length_str) 
                            ln = line[:22]+length_str+line[32:] 
                            err_id_f.write("length_ERROR_")
                            err_id_f.write(length_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==11):
                            Tag =err_eij_hdl.pcie_Tag_err_eij()
                            Tag_str=format(Tag, '08b')
                            #print(Tag_str)
                            #ln = TH_str+line[:15]
                            ln = line[:48]+Tag_str+line[56:]
                            err_id_f.write("Tag_ERROR_")
                            err_id_f.write(Tag_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==12):
                            Last_DW_BE =err_eij_hdl.pcie_Last_DW_BE_err_eij()
                            Last_DW_BE_str=format(Last_DW_BE, '04b')
                            #print(Last_DW_BE_str)
                            #ln = TH_str+line[:15]
                            ln = line[:56]+LastDW_BE_str+line[60:]
                            err_id_f.write("Last_DW_BE_ERROR_")
                            err_id_f.write(Last_DW_BE_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==13):
                            First_DW_BE =err_eij_hdl.pcie_First_DW_BE_err_eij()
                            First_DW_BE_str=format(First_DW_BE, '05b')
                            #print(First_DW_BE_str)
                            ln = line[:60]+First_DW_BE_str+line[64:]
                            err_id_f.write("First_DW_BE_ERROR_")
                            err_id_f.write(First_DW_BE_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==14):
                            completion_Id =err_eij_hdl.pcie_completion_Id_err_eij()
                            completion_Id_str=format(completion_Id, '16b')
                            #print(completion_Id_str)
                            ln = line[:64]+completion_Id_str+line[80:]
                            err_id_f.write("completion_ID_ERROR_")
                            err_id_f.write(completion_Id_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==15):
                            Ext_Register_Num =err_eij_hdl.pcie_Ext_Register_Num_err_eij()
                            Ext_Register_Num_str=format(Ext_Register_Num, '4b')
                            #print(Ext_Register_Num_str)
                            ln = line[:84]+Ext_Register_Num_str+line[88:]
                            err_id_f.write("Ext_Register_Num_ERROR_")
                            err_id_f.write(Ext_Register_Num_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==16):
                            Register_Num =err_eij_hdl.pcie_Register_Num_err_eij()
                            Register_Num_str=format(Register_Num, '6b')
                            #print(Register_Num_str)
                            ln = line[:88]+Register_Num_str+line[94:]
                            err_id_f.write("Register_num_ERROR_")
                            err_id_f.write(Register_Num_str)
                            err_id_f.write(str(err_id_q[self.k][self.m]))
                            err_id_f.write("\n")
                            err_id_f.write(ln)
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
 
                        self.k=self.k+1
                    # else statemnet: if "m"th iteration is not present in err_array then it will 0 
                    else:
                        err_id_f.write(line)
                        err_id_f.write("\n")
                        err_bin_f.write(line)
                        pkt_queue.put(line)

            else:
                err_id_f.write(line)
                err_id_f.write("\n")
                err_bin_f.write(line)
                pkt_queue.put(line)
            #contents[self.m] = ln 
            self.m=self.m+1
            err_bin_f.write("\n")
            err_id_f.write("\n")

        err_bin_f.close()
        bin_f.close()

p = pcie_rc_driver()
#tx = pcie_seq_rc_config_pkt()
#for i in range(num_pkts):
#tx.cfg0_pkt() 
p.drive_tx()
#p.err_eij_file_handle()
#with open("err_bin_file.txt","w") as file:
#    file.writelines(contents)
#err_bin_f.close()
err_id_f.close() 
from pcie_rc_tx_monitor import *



