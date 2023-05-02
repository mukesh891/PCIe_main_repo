import sys
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/rc_src/")
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/")
#import time
#from pcie_base_test import *
from pcie_rc_tx_item import *

import fcntl
from pcie_pkt_checker import checker_pkt

class tb_top:
    print("1. This is tb top class")

#time.sleep(5)
c= checker_pkt()
c.checker_fn()

## TODO: Clk gen and Reset Declaration 
    # clk=0
    # rst=0

## TODO: Instantaiating Wrapper Class 

## TODO: MIMIC run_test() aand ##
    #Currently only running the generation part of RC
    #pcie_rc_cfg0_pkt

## TODO: Dumping data to get waveform

## TODO: Start and End of simulation statements
    #sys.exit() after certain time period

