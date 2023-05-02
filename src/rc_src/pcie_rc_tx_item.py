import sys
import re 
import random
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/")
from pprint import pprint
from pcie_tx_item import pcie_tx_item
from pcie_config_obj import *

import fcntl
import os 

class pcie_rc_tx_item(pcie_tx_item):
    print("2. This is pcie_rc_tx_item class")
    def __init__(self):
      super().__init__()

