import queue
from pcie_lib import *
from pcie_com_file import *

###### Giving info about the log files###############
logger.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_com_file.py file")

base_rec_queue = queue.Queue()
pkt_with_flag_queue = queue.Queue()
ep_to_rc_queue = queue.Queue()