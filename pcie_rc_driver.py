from pcie_lib import *
from pcie_com_file import *
#from err_id_creation import *

from pcie_rc_config_pkt import *
logging.info("Entering Driver class of ROOT COMPLEX ")

from pcie_rc_callback import *

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
            if(err_eij):
                if(self.m<num_pkts):
                    logging.info("Entering err_eij if statement ")
                    err_eij_hdl = pcie_err_eij()
                    if self.m in arr:
                        print("m in arr",self.m)
                        #if(self.k == self.m):
                        #if(m==self.k):
                        logging.info("Entering err_eij array to inject ")
                        ## randomly choose between bdf and fmt err
                        j = random.choice([0,1,2])
                        j = 1 
                        if(j==0):
                            print(str(bin(err_eij_hdl.pcie_requester_id_err_eij())))
                            r_id = str(bin(err_eij_hdl.pcie_requester_id_err_eij()))
                            ln = str(line[:32])+str(r_id)+line[48:]
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                        if(j==1):
                            fmt = err_eij_hdl.pcie_fmt_err_eij()
                            fmt_str                 =format(fmt, '03b')       
                            print("modified fmt->",fmt_str) 
                            ln =fmt_str+line[3:]
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                            
                        if(j==2):
                            typ =err_eij_hdl.pcie_type_err_eij()
                            type_str                 =format(typ, '05b')       
                            print(typ_str) 
                            ln = line[:3]+str(typ)+line[8:] 
                            err_bin_f.write(ln)
                            pkt_queue.put(ln)
                    else:
                        err_bin_f.write(line)
                        pkt_queue.put(line)

            else:
                err_bin_f.write(line)
                pkt_queue.put(line)
            #contents[self.m] = ln 
            #err_bin_f.write("\n")


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



