import sys
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/")
from pcie_lib import *
from pcie_tx_item import pcie_tx_item
from pcie_config_obj import *

class pcie_ep_tx_item(pcie_tx_item):
    print("2. This is pcie_ep_tx_item class")
    def __init__(self):
      super().__init__()

