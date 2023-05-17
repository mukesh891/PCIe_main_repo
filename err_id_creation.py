## enum.py
from pcie_com_file import *
err_pkt_no = argv.err_pkt_no
err_id_q = [] 
packet_errors = {} 
print(arr)
for i in arr:
    packet_errors = {
    i: "ERR_ID_"+str(i)
    }
    print(packet_errors)
    err_id_q.append(packet_errors)
    print(err_id_q)


print(packet_errors)

for j in err_id_q:
    print(j)
