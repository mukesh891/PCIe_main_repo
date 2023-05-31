from pcie_rc_config_pkt import *
from pcie_rc_mem_seq import *
from pcie_com_file import *
from pcie_rc_com_file import *
from pcie_rc_generated_logs import *

logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX : Compiling pcie_rc_base_test.py file")

class pcie_rc_base_test:
    def __init__(self):
        num_pkts = argv.num_pkts
        super().__init__()
        self.which_seq = 0
    
    def run(self, test_name):
        # Dynamically retrieve the method based on the provided test_name
        method = getattr(self, test_name, None)
        
        if method is not None and callable(method):
            # Call the retrieved method with the necessary arguments
            method()
        else:
            print(f"Method '{test_name}' not found or not callable.")

class basic_seq_test(pcie_rc_base_test):
    def run(self, test_name):
        super().run(test_name)

    def cfg_test(self):
        logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX: RUNNING \"cfg_seq_test\"")
        print("---cfg test")
        for i in range(num_pkts):  # as we are sending 128 bits
            mem_seq.run_mem()

    def cfg_with_mem_seq_test(self):
        logging.info(f"{formatted_datetime} \t\t\tROOT COMPLEX: RUNNING \"cfg_with_mem_seq_test\"")
        for i in range(num_pkts):  # as we are sending 128 bits
            # First 10 packets have to be config type
            if i > 9:
                mem_seq.run_mem()
            else:
                cfg_seq.run_cfg()

cfg_seq = pcie_rc_config_pkt()
mem_seq = pcie_rc_mem_seq()
basic_test = basic_seq_test()
basic_test.run(test)

g_log=pcie_rc_generated_logs()
g_log.bin_file_handle()
g_log.hex_file_handle()
g_log.gen_log()
g_log.mem_rd_file_handle()

