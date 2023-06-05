from pcie_ep_cfg_pkt import *
from pcie_ep_mem_pkt import *
from pcie_com_file import *

logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_pkt_transmitter.py file")
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For Generation of CFG/MEM TLP in Binary : ep_logs/ep_tx_send_pkt_bin.txt")

tx_send_ep_bin = open('ep_logs/ep_tx_send_pkt_bin.txt', 'w')
#total_pkts = 0


class pcie_ep_pkt_transmitter:
    def cfg_mem_tx_fn(self, pkt_num):
        if(pkt_num < 4):
            TLP = pcie_ep_cfg_pkt.cfg_tx_fn(self, pkt_num)
            #total_pkts += 1
        else:
            TLP = pcie_ep_mem_pkt.mem_tx_fn(self, pkt_num)
            #total_pkts += 1
        

        tx_send_ep_bin.write('{}\n'.format(TLP))
        return TLP

    
            

