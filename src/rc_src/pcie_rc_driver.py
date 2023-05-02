#import sys
#sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/rc_src")
#import logging
#logging.basicConfig(level=logging.DEBUG)
from pcie_lib import *
from pcie_config_obj import *
logging.info("Entering Driver class of ROOT COMPLEX ")

from pcie_rc_config_base import pcie_rc_cfg0_pkt

from pcie_rc_callback import *

class pcie_rc_driver:
    def drive_tx(self):
        err_eij = argv.err_eij
        logging.info("Entering Driver class of ROOT COMPLEX ")
        print("in driver class modified bdf BEFORE eij->",tx.bdf)
        ## INFO :Erro injection using commandline arg "--err_eij=1" ##
        if(err_eij):
            logging.info("ERROR INJECTION SUCCESSFUL AT THE DRIVER END")
            bdf_cb = pcie_bdf_err_eij()
            tx.bdf = bdf_cb.bdf_eij_err()
            print("in driver class modified bdf AFTER eij->",tx.bdf)
        
        print(err_eij)
tx=pcie_rc_cfg0_pkt()
p = pcie_rc_driver()
p.drive_tx()

