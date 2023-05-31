import queue
from pcie_com_file import *

###### Giving info about the log files###############
logging.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_com_file.py file")

#pkt_valid_queue = queue.Queue()
pkt_with_flag_queue = queue.Queue()