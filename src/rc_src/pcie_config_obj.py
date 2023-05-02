import os
import argparse
cwd = os.getcwd()
class pcie_config_obj:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--num_pkts', type= int , help = 'Total num of packets to be generated at generator side and must be positive value', default = 10)
        parser.add_argument('--err_eij', type= int , help = 'A bit value to represent error injection is done or not and must be 0,1', default = 0)
        
        return parser.parse_args()
c=pcie_config_obj
argv = pcie_config_obj.parse_args()
#num_pkts = argv.num_pkts
#class ex:
#    def __init__(self):
        
#obj=ex()
#print(num_pkts)


