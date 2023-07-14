from pcie_ep_cfg_pkt import *
from pcie_ep_mem_pkt import *
from pcie_com_file import *

logger.info(f"{formatted_datetime} \t\t END-POINT : Compiling pcie_ep_pkt_transmitter.py file")
logger.info(f"{formatted_datetime} \t\t END-POINT : Creating log For Generation of CFG/MEM TLP in Binary : ep_logs/ep_tx_send_pkt_bin.txt")

tx_send_ep_bin = open('ep_logs/ep_tx_send_pkt_bin.txt', 'w')
#total_pkts = 0

ep_mem_pkt = pcie_ep_mem_pkt()

class pcie_ep_pkt_transmitter:
    def cfg_mem_tx_fn(pkt_num):
        if(pkt_num < 4):
            TLP = pcie_ep_cfg_pkt.cfg_tx_fn(pkt_num)
            logger.info(f"{formatted_datetime} \t\t\t END-POINT : RUNNING \"ep_cfg_tx_fn\"")
            #tx_send_ep_bin.write('\npkt num for cfg {}\n'.format(pkt_num))
            #total_pkts += 1
        else:
            TLP = ep_mem_pkt.mem_tx_fn(pkt_num)
            logger.info(f"{formatted_datetime} \t\t\t END-POINT : RUNNING \"ep_mem_tx_fn\"")
            #tx_send_ep_bin.write('\npkt num for mem {}\n'.format(pkt_num))
            #total_pkts += 1
        tx_send_ep_bin.write('{}\n'.format(TLP))
        
        if delay_en:
                random_delay = 0.5 #random.uniform(1, 2)
                time.sleep(random_delay)
        else:
                print("no delay")

        return TLP

    
            

