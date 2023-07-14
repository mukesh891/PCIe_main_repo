from pcie_com_file import *
from pcie_ep_base import *
import random
from tabulate import tabulate
from pcie_com_file import *
from pcie_ep_cfg_pkt import *

logger.info(f"{formatted_datetime} \t\t\t END-POINT : Compiling pcie_ep_mem_pkt.py file")
#logger.info(f"{formatted_datetime} \t\t\t END-POINT : Creating log For Generation of MEM TLP : ep_logs/ep_mem_pkt.txt")

dict_mem = {}


#mem_tx = open('ep_logs/ep_mem_pkt.txt', 'w')

class pcie_ep_mem_pkt(ep_base_pkt):
    def __init__(self):
        #super.__init__(self)
        self.chunk_data	= []
        self.i = 0
        self.j = 0
        self.iter = 0
        self.temp_length = 0
        self.rd_temp_addr = 0
        self.wr_temp_addr = 0
    def mem_tx_fn(self,pkt_num):
        Fmt = random.choice([0, 2])	
        Type = random.choice([0])	
        T9 = 0
        TC = 0
        T8 = 0
        Attr1 = 0
        LN = 0
        TH = 0
        TD = 0
        EP = 0
        Attr0 = 0
        AT = 0
        Length = 18 
        Requester_Id = 540
        Tag = 0

        if(Fmt == 2):
            Payload = random.getrandbits(32*Length)
        else:
            Payload = 0
        if(DW % mps == 0):
            self.num_tx     = DW//mps 
            pass
        else:
            self.num_tx     = DW // mps + 1

        for j in range(self.num_tx): 
                ## Storing the payload data in chunk_data array for later num_txs
            if(len(self.chunk_data) == 0):
                data_payload_size   = f'0{32*DW}b'
                remaining_dw        = DW%mps
                Payload   = random.getrandbits(32*Length)
                Payload_str         =  format(Payload, data_payload_size)
                num_split = len(Payload_str)//(32*mps)
                Address = random.getrandbits(30)
                Address     = random.randint(0,63)
                
                ## randomizing the address for 1 tx and will be executed once in every write tx
                Requester_Id           = random.getrandbits(16)
                Tag                     = random.getrandbits(8)
                
                Address -= Address % 4  #The purpose of this code is to ensure that self.addresses is a multiple of 4 or 4 byte aligned
                self.temp_length = Length
                self.wr_temp_addr = Address
                self.rd_temp_addr = Address
                for j in range(num_split):
                    self.chunk_data.append(Payload_str[(j*mps*32) :(j+1)*mps*32])
                if remaining_dw:
                    self.chunk_data.append(Payload_str[len(Payload_str)-(remaining_dw*32):])
             
            ## calculate the num of tx depending upon the length of data and mps
             
            #logger.info("################  num tx = {}  ###############\n".format(self.num_tx))
            if(self.iter % 2 == 0):
                if self.i < self.num_tx:
                    Fmt = 2
                    Last_DW_BE = random.getrandbits(4)
                    First_DW_BE = random.getrandbits(4)
                    dict_mem['Last_DW_BE'] = Last_DW_BE
                    dict_mem['First_DW_BE'] = First_DW_BE
                    Payload_str            = self.chunk_data[self.i]
                    if(self.i==0):
                        pass
                    else:
                        Length              =   Length - mps
                        Address             =  self.wr_temp_addr + mps
                self.i+=1
              
              
            else:
                Fmt = 0
                Address =  self.rd_temp_addr
                Last_DW_BE = dict_mem['Last_DW_BE']
                First_DW_BE = dict_mem['First_DW_BE']
                self.chunk_data.clear()
                self.iter += 1
                data_payload_size   = f'0{32}b'
                Payload_str            = format(0, data_payload_size)
            Rsv_11_1 = 0
            Fmt_str = format(Fmt, '03b')
            Type_str = format(Type, '05b')
            T9_str = format(T9, '01b')
            TC_str = format(TC, '03b')
            T8_str = format(T8, '01b')
            Attr1_str = format(Attr1, '01b')
            LN_str = format(LN, '01b')
            TH_str = format(TH, '01b')
            TD_str = format(TD, '01b')
            EP_str = format(EP, '01b')
            Attr0_str = format(Attr0, '02b')
            AT_str = format(AT, '02b')
            Length_str = format(Length, '010b')
            
            Requester_Id_str = format(Requester_Id, '016b')
            Tag_str = format(Tag, '08b')
            Last_DW_BE_str = format(Last_DW_BE, '04b')
            First_DW_BE_str = format(First_DW_BE, '04b')
            
            Address_str = format(Address, '030b')
            Rsv_11_1_str = format(Rsv_11_1, '02b')
            
            Length_size = '0' + str(32*DW) + 'b'
            
            
            #Payload_str = format(Payload, Length_size)
            
            TLP = Fmt_str + Type_str + T9_str + TC_str + T8_str + Attr1_str + LN_str + TH_str + TD_str + EP_str + Attr0_str + AT_str + Length_str + Requester_Id_str + Tag_str + Last_DW_BE_str +First_DW_BE_str + Address_str + Rsv_11_1_str + Payload_str
            
            
            if(TD == '1'):
                ECRC = int(TLP, 2) % int(fixed_ecrc_divisor, 2)
                TLP = TLP + format(ECRC, '032b')
            else:
                ECRC = None
                TLP = TLP

            ep_to_rc_queue.put(TLP)
            
            
            
            
            pkt_tlp_tb = [[ Fmt_str, Type_str, T9_str, TC_str, T8_str, Attr1_str, LN_str, TH_str, TD_str, EP_str, Attr0_str, AT_str, Length_str, Requester_Id_str, Tag_str, Last_DW_BE_str, First_DW_BE_str, Address_str,Rsv_11_1_str,Payload_str, ECRC, '']]
            names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Address_str','Rsv_11_1','Payload_str', 'ECRC', '']
            table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
            #mem_tx.write('MEMORY TLP {} : {}\n\n'.format(pkt_num, TLP))
            #mem_tx.write(table)
            #mem_tx.write('\n\n\n\n')
            #logger.info("## tx = {}  ##\n".format(TLP))
            
            #tx_send_ep.write('EP_TRANSMITTING MEMORY TLP {} : {}\n\n'.format(pkt_num, TLP))
            tx_send_ep.write('EP_TRANSMITTING MEMORY TLP {} : {}\n\n'.format(pkt_num, TLP))
            tx_send_ep.write(table)
            tx_send_ep.write('\n\n\n\n\n')
            if(self.i==self.num_tx):
                self.i = 0
                self.iter = self.iter+1 
            #print('start of mem ep_tx {}'.format(pkt_num))
            #print('TLP {}'.format(TLP))
            self.j += 1
        
            return TLP
