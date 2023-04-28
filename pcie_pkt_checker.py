import random
from pcie_com_file import *

print("checker block")

class checker_pkt():


	def checker_fn(self):
		#bdf, conf_type, block, ep, td = packet_check
		block = pkt_dict.get("block")
		bdf = pkt_dict.get("bdf")
		conf_type = pkt_dict.get("conf_type")
		ep = pkt_dict.get("ep")
		td = pkt_dict.get("td")
		data = pkt_dict.get("data")
		fmt = pkt_dict.get("fmt")
		tc = pkt_dict.get("tc")
		attr = pkt_dict.get("attr")
		th = pkt_dict.get("th")
		at = pkt_dict.get("at")
		length = pkt_dict.get("length")  # no data , will print None
		first_dw_be = pkt_dict.get("first_dw_be")
		name = pkt_dict.get("name")
		size_in_bytes = pkt_dict.get("size_in_bytes")
		xwr = pkt_dict.get("xwr")
		


		print('checker_fn BDF = {}, config type {} for {}, {}, pkt is {}, ECRC is {}, Data is {}, fmt is {}, tc is {}, attr is {}, tlp hint is {}, address translation is {}, length is {}, first_dw_be is {}, name is {}, size in bytes, xwr is {}'
		.format(bdf, conf_type, "Switch" if conf_type else "end-point", "Blocking" if block else "Non-blocking", "Poisoned" if ep else "Not poisoned", "Enabled" if td else "Disabled", data, fmt, tc, attr, th, at, length, first_dw_be, name, size_in_bytes, xwr))
        
		if not (0 <= fmt < 2**3 and 0 <= bdf < 2**16 and 0 <= conf_type <= 1 and 0 <= ep <= 1 and 0 <= td <= 1 and 0 <= block <= 1):
			print("Packet is invalid due to:")
			if(bdf >= 2**16):
				print('INVALID BDF, value: {}'.format(bdf))
			if(fmt >= 2**16):
				print('INVALID FMT, value: {}'.format(fmt))
		

			
			return False
		else:
			print("Packet is valid")
			return True