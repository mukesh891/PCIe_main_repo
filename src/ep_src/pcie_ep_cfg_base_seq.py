import sys
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/")
from pcie_lib import *
from pcie_ep_tx_item import *
from pcie_config_obj import *

print("hello pcie_ep_cfg_base_seq")

class pcie_ep_cfg_base_seq(pcie_ep_tx_item):
    print("2. This is pcie_ep_cfg_pkt")
    def __init__(self):
        super().__init__()
    
