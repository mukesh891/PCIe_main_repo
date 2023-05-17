from pcie_lib import *
#from pcie_com_file import *
from err_id_creation import *

from pcie_rc_config_pkt import *
logging.info("Entering Driver class of ROOT COMPLEX ")

from pcie_rc_callback import *
err_id_f = open("gen_logs/error_id_file.txt","w") 
bin_f = open("gen_logs/bin_file.txt","r") 
err_bin_f = open("gen_logs/err_bin_file.txt","w")
class pcie_rc_driver:
    def __init__(self):
        self.k=0
        self.m=0
    def drive_tx(self):
        num_pkts= argv.num_pkts
        ln = ""
        logging.info("Entering Driver class of ROOT COMPLEX ")
        ## INFO :Erro injection using commandline arg "--err_eij=1" ##
        for line in bin_f:
            #line = re.sub(line,' ','')
            line = line.strip('\n')
            print("binfile line[0]",line)
            print("length of line",len(line))
            # error injection enable
            if(err_eij):
                # m is no. of iterations till num_pkts-1
                if(self.m < num_pkts):
                    print(self.m)
                    # err_id_q is an array with size of err_pkt_no, You can get "err_pkt_no" and err_id_q in pcie_com_file.py
                    # checking whether m is lessthan the no. of erroe pkts injected
                    if(self.m < len(err_id_q)):
                        print("error id for the injection is-> ",err_id_q[self.m])
                        err_id_f.write("error id for the injection is-> ")
                        err_id_f.write(str(err_id_q[self.m]))
                        err_id_f.write("\n")

                    logging.info("Entering err_eij if statement ")
                    err_eij_hdl = pcie_err_eij()
                    if self.m in arr:
                        print("m in arr",self.m)
                        logging.info("Entering err_eij array to inject ")
                        ## randomly choose between bdf and fmt and type error
                        j = random.choice([0,1])
                        # If j==1 , then "fmt" will be injected with error 
                        if(j==1):
                            fmt = err_eij_hdl.pcie_fmt_err_eij()
                            fmt_str                 =format(fmt, '03b')       
                            print("modified fmt->",fmt_str) 
                            ln =fmt_str+line[3:]
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                            
                        # If j==0 , then "type" will be injected with error
                        if(j==2):
                            typ =err_eij_hdl.pcie_type_err_eij()
                            type_str=format(typ, '05b')       
                            print(type_str) 
                            ln = line[:3]+type_str+line[8:] 
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                    else:
                        err_bin_f.write(line)
                        pkt_queue.put(line)

            else:
                err_bin_f.write(line)
                pkt_queue.put(line)
            #contents[self.m] = ln 
            err_bin_f.write("\n")


            self.m=self.m+1
        err_bin_f.close()

p = pcie_rc_driver()
#tx = pcie_seq_rc_config_pkt()
#for i in range(num_pkts):
#tx.cfg0_pkt() 
p.drive_tx()
#p.err_eij_file_handle()
#with open("err_bin_file.txt","w") as file:
#    file.writelines(contents)
bin_f.close()
err_bin_f.close()
err_id_f.close() 


