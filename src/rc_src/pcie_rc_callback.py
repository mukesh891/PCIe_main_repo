from pcie_rc_config_base import pcie_rc_cfg0_pkt

from pprint import pprint
class pcie_callbacks:
    print("This is pcie callback class")

class pcie_bdf_err_eij(pcie_callbacks):
    print("This is BDF error injection class")
    def bdf_eij_err(self):
        print("This is bdf eij err callback ")
        #pkt.cfg0_pkt()
        tl_pkt=pcie_rc_cfg0_pkt()
        tl_pkt.bdf=50
        print(tl_pkt.bdf)
        return tl_pkt.bdf

		
