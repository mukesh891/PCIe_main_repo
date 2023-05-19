from pcie_rc_config_pkt import *
from pcie_rc_mem_seq import *
from pcie_com_file import *
from pcie_rc_com_file import *
from pcie_rc_generated_logs import *
class pcie_rc_base_seq:
    def __init__(self):
        num_pkts = argv.num_pkts
        super().__init__()
        self.which_seq = 0
    def run(self):
        print("Main sequence executed")
        cfg_seq = pcie_rc_config_pkt()
        mem_seq = pcie_rc_mem_seq()
        for i in range(num_pkts): # as we are sending 128bits
            #First 10 packets has be config type
            if(i > 9):     
                mem_seq.run_mem()
            else:
                cfg_seq.run_cfg()
            #    if __name__ == "__main__":
            #        seq.run()
#for i in range(g_pkt_queue.qsize()):
#            bin_q = g_pkt_queue
#            q = bin_q.get()
#            print("the g pkt q is ->",q)

base_seq =pcie_rc_base_seq()
base_seq.run()
bin_f.close()        
g_log=pcie_rc_generated_logs()
g_log.bin_file_handle()
g_log.hex_file_handle()

