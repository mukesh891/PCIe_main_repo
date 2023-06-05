from tabulate import tabulate

err_bin_compl2 = open("ep_logs/pcie_final_ep_tx_table_file.txt","w")

class pcie_final_ep_tx_table_file:
    def pcie_final_ep_tx_table_fn(num, TLP):
        Fmt = TLP[0:3]
        Type = TLP[3:8]
        T9 = TLP[8]
        TC = TLP[9:12]
        T8 = TLP[12]
        Attr1 = TLP[13]
        LN = TLP[14]
        TH = TLP[15]
        TD = TLP[16]
        EP = TLP[17]
        Attr0 = TLP[18:20]
        AT = TLP[20:22]
        Length = TLP[22:32]

        Requester_Id = TLP[32:48]
        Tag = TLP[48:56]
        Last_DW_BE = TLP[56:60]
        First_DW_BE = TLP[60:64]

        if (Type[2] == '1'):            # for cfg
                Requester_Id = TLP[32:48]
                Tag = TLP[48:56]
                Last_DW_BE = TLP[56:60]
                First_DW_BE = TLP[60:64]
                Completion_Id = TLP[64:80]
                Rsv_10_7 = TLP[80:84]       # reserved byte 10- bit 7:4
                Ext_Register_Num = TLP[84:88]
                Register_Num = TLP[88:94]
                Rsv_11_1 = TLP[94:96]       # reserved byte 11- bit 1:0
        elif(Type[:-1] == '0000'):      # for memory
                Requester_Id = TLP[32:48]
                Tag = TLP[48:56]
                Last_DW_BE = TLP[56:60]
                First_DW_BE = TLP[60:64]
                Address = TLP[64:94]
                Rsv_11_1 = TLP[94:96] 
        elif(Type == '01010'):            
                Completion_Id = TLP[32:48]
                Compl_status = TLP[48:51]      # status 3 if some occured in completer
                BCM = TLP[51]                  # only be set by PCI-x, so for PCIe its always 0
                Byte_count = TLP[52:64]        # excluding memory read compl & atomic compl, byte count must be 4

                Requester_Id = TLP[64:80]       # must be same as request
                Tag = TLP[80:88]                # must be same as request       
                Rsv_11_7 = TLP[88]              # byte 11 bit 7 is reserved
                Lower_address = TLP[89:96]
                
			
        Header = TLP[0:96]
        Data = TLP[96:]

        if (Type[2] == '1'):            # for cfg
                pkt_tlp_tb = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Completion_Id,Rsv_10_7, Ext_Register_Num, Register_Num,Rsv_11_1,Data, '']]
                names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Completion_Id','Rsv_10_7', 'Ext_Register_Num', 'Register_Num','Rsv_11_1','Data', '']
                table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
                err_bin_compl2.write('EP_TRANSMITTING {} TLP {} : {}\n\n'.format('CFG', num, TLP))
                err_bin_compl2.write(table)
                err_bin_compl2.write('\n\n\n\n\n')
            #log_file.write(table)
        elif(Type[:-1] == '0000'):      # for memory
                pkt_tlp_tb = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Requester_Id, Tag, Last_DW_BE, First_DW_BE, Address, Rsv_11_1,Data, '']]
                names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length', 'Requester_Id', 'Tag', 'Last_DW_BE', 'First_DW_BE', 'Address','Rsv_11_1','Data', '']
                table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
                err_bin_compl2.write('EP_TRANSMITTING {} TLP {} : {}\n\n'.format('MEMORY', num, TLP))
                err_bin_compl2.write(table)
                err_bin_compl2.write('\n\n\n\n\n')
        elif(Type == '01010'):      # for memory
                pkt_tlp_tb = [[ Fmt, Type,T9, TC, T8, Attr1, LN, TH, TD, EP, Attr0, AT, Length, Completion_Id, Compl_status,BCM,Byte_count, Requester_Id,Tag,Rsv_11_7,Lower_address,'']]
                names = [ 'Fmt', 'Type', 'T9', 'TC', 'T8', 'Attr1', 'LN', 'TH', 'TD', 'EP', 'Attr0', 'AT', 'Length','Completion_Id', 'Compl_status', ' BCM' ,'Byte_count', 'Requester_Id', 'Tag','Rsv_11_7', 'Lower_address', '']
                table = tabulate(pkt_tlp_tb, headers=names, tablefmt='orgtbl')
                err_bin_compl2.write('EP_TRANSMITTING {} TLP {} : {}\n\n'.format('COMPLETION', num, TLP))
                err_bin_compl2.write(table)
                err_bin_compl2.write('\n\n\n\n\n')