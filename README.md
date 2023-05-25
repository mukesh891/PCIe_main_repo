# PCIe
Command line for running the main.py file:
  
$ python3 main.py --num_pkts=20 --err_eij=1 --err_pkt_no=10 --ep_err_eij=1 --ep_err_pkt_no=5
  
[By default num_pkts = 100, err_eij = 0, err_pkt_no = 0, ep_err_eij = 0, ep_err_pkt_no = 0]
    
>>num_pkts          ->Declared as int datatype  
                    ->Total no. of packets you need to be generate
    
>>err_eij           ->Declared as bit datatype
                    ->Used for Enabling or Disabling the error injection
    
>>err_pkt_no        ->Declared as bit datatype
                    ->Total no. of error packets need to be injected
                    
>>ep_err_eij        ->Declared as bit datatype
                    ->Used for Enabling or Disabling the error injection from completer
    
>>ep_err_pkt_no     ->Declared as bit datatype
                    ->Total no. of error packets need to be injected from completer
                    
                    
                    
                    
                    
Libraries used:

Arguments used:

Output files Generated:

How RC Side Generator Works:

How EP Side Checker Works:

ERROR INJECTION ENABLING:

