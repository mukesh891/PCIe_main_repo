import re
import random
import fcntl
print("checker block")

class checker_pkt():
    def checker_fn(self):
        try:
            with open("/home/mukesh/PCIe/PCIe_repo/src/rc_src/Hex_file.txt",'r') as f:
                #fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                for line in f:    
                    ## Removing white spaces from file ##
                    int_val = int(line,16)
                    bin_val = bin(int_val)
                    bin_s = str(bin_val)
                    bin_str = re.sub("^0b",'',bin_s)
                    #line = re.sub(" ","",line)
                    print(line,"->",bin_s,"->" , bin_str[len(bin_str)-4:len(bin_str)])
                    transaction_type =bin_str[0:7)
                    print(transaction_type)
        except FileNotFoundError:
            print("The file could not be found.")
        except IOError:
            print("An error occurred while reading the file.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
        finally:
            print("Done with file operations.")
c=checker_pkt()
c.checker_fn()
                #bdf, conf_type, block, ep, td = packet_check
                #block = pkt_dict.get("block")
		    	#bdf = pkt_dict.get("bdf")
		    	#conf_type = pkt_dict.get("conf_type")
		    	#ep = pkt_dict.get("ep")
		    	#td = pkt_dict.get("td")
		    	#data = pkt_dict.get("data")
		    	#fmt = pkt_dict.get("fmt")
		    	#tc = pkt_dict.get("tc")
		    	#attr = pkt_dict.get("attr")
		    	#th = pkt_dict.get("th")
		    	#at = pkt_dict.get("at")
		    	#length = pkt_dict.get("length")  # no data , will print None
		    	#first_dw_be = pkt_dict.get("first_dw_be")
		    	#name = pkt_dict.get("name")
		    	#size_in_bytes = pkt_dict.get("size_in_bytes")
		    	#xwr = pkt_dict.get("xwr")
#                print('checker_fn BDF = {}\n' 'config type = {} for {}\n' '{}, pkt = {}\n' 'ECRC = {}\n' 'Data = {}\n' 'fmt = {}\n' 'tc = {}\n' 'attr = {}\n' 'tlp hint = {}\n' 'address translation = {}\n' 'length = {}\n' 'first_dw_be = {}\n' 'name = {}\n' 'size in bytes = {}\n' 'xwr = {}\n' .format(bdf , conf_type, "Switch" if conf_type else "end-point", "Blocking" if block else "Non-blocking", "Poisoned" if ep else "Not poisoned","Enabled" if td else "Disabled", data, fmt, tc, attr, th, at, length, first_dw_be,name, size_in_bytes, xwr))
#
#
#
#		
#		with open('output_checker.txt', 'a') as f:
#			f.write('checker_fn BDF = {}\n' 'config type = {} for {}\n' '{}, pkt = {}\n' 'ECRC = {}\n' 'Data = {}\n' 'fmt = {}\n' 'tc = {}\n' 'attr = {}\n' 'tlp hint = {}\n' 'address translation = {}\n' 'length = {}\n' 'first_dw_be = {}\n' 'name = {}\n' 'size in bytes = {}\n' 'xwr = {}\n' .format(bdf , conf_type, "Switch" if conf_type else "end-point", "Blocking" if block else "Non-blocking", "Poisoned" if ep else "Not poisoned","Enabled" if td else "Disabled", data, fmt, tc, attr, th, at, length, first_dw_be,name, size_in_bytes, xwr))
#
#
#		if not (0 <= fmt < 2**3 and 0 <= bdf < 2**16 and 0 <= conf_type <= 1 and 0 <= ep <= 1 and 0 <= td <= 1 and 0 <= block <= 1):
#			print("Packet is invalid due to:")
#			if(bdf >= 2**16):
#				with open('output_checker.txt', 'a') as f:
#					f.write('INVALID BDF, value: {}\n'.format(bdf))
#				print('INVALID BDF, value: {}'.format(bdf))
#			if(fmt >= 2**3):
#				with open('output_checker.txt', 'a') as f:
#					f.write('INVALID FMT, value: {}\n'.format(fmt))
#				print('INVALID FMT, value: {}'.format(fmt))
#		
#
#			
#			return False
#		else:
#			print("Packet is valid")
#			with open('output_checker.txt', 'a') as f:
#				f.write('Packet is valid\n')
#			return True
