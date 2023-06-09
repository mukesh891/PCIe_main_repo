## enum.py
from pcie_rc_com_file import *
err_pkt_no = argv.err_pkt_no
err_id_q = [] 
packet_errors = {} 
arr=[]
if(err_eij): 
    while len(arr) < err_pkt_no:
        num = random.randrange(0,num_pkts-1)
        if num not in arr:
            arr.append(num)
        arr.sort()

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
