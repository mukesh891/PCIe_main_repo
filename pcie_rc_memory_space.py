import logging,os
#os.system("rm -rf /gen_logs/memory.txt")
#with open("/gen_logs/memory.txt", "w") as file:
#    print("file created")
def write_modify_data(address,data,length):

    def is_address_present(address):
        with open("gen_logs/memory.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    line_address, data = line.strip().split()
                #print(int(line_address,16))
                    if int(line_address,16) == address:
                        print("check for address  line_address macth", address, line_address)
                        return True
        return False

    def write_data_to_mem_space(address, data, length):
        with open("gen_logs/memory.txt", "a") as file:
            #bin_data = bin(data)[2:].zfill(length * 32)
            length = int(str(length),2)
            hex_data = hex(int(data,2))[2:].zfill(length * 2)
            len_data = len(data)//32
            if(len_data == length ):
                for i in range(0, len(hex_data), 2):
                    byte = str(hex_data[i:i + 2])
                    #file.write(f"0x{address + i // 2:02X} 0x{byte}\n")
                    file.write("0x{:02X} 0x{}\n".format(int(address,2) + i // 2, byte))
            else:
                logging.error("Write data fn: Inavlid length or data entered, length = {}dw , len_data = {}dw, hex data = {}, bin_data = {}".format(length,len_data,hex_data,data))

    def modify_data_in_mem_space(address, data, length):
        with open("gen_logs/memory.txt", "r") as file:
            lines = file.readlines()

        with open("gen_logs/memory.txt", "r+") as file:
            #bin_data = bin(data)[2:].zfill(length * 32)
            hex_data = hex(int(data,2))[2:].zfill(length * 2)
            len_data = len(data[2:])
            if len_data == length * 32:
                for i in range(0, len(hex_data), 2):
                    #print("Modifying address  data length", address,data,length)
                    byte = hex_data[i:i + 2]
                    file.write(f"0x{address + i // 2:02X} 0x{byte}\n")
            else:
                logging.error("Modified data fn: Invalid length or data entered, Length = {}B, Data Width = {}b, data = {}, bin_data = {}".format(length, len_data, hex_data, data))
                        
    if is_address_present(address):
        print("Modifying address ", address)
        modify_data_in_mem_space(address, data, length)
    else:
        write_data_to_mem_space(address, data,length)


def read_data_from_mem_space(address, length):
    address = int(address,2)
    length = int(length,2)
    #length = 2
    #with open("gen_logs/memory.txt", "a") as file:
    #    file.write("Reading data fn: address fetched = {}, length = {}".format(address,length))

    data_chunk = []
    with open("gen_logs/memory.txt", "r") as file:
        file.seek(0)  # Move the file pointer to the beginning of the file
        lines = file.readlines()
        for line in lines:
            line_address, value = line.strip().split()
            if address <= int(line_address, 16) < address + (length * 4):
                data_chunk.append(int(value,16))  # Convert hexadecimal value to integer
    print(data_chunk)
    data = ''.join(format(value, '08b') for value in data_chunk)
    logging.info("data sent from mem space = {}".format(data))
    #with open("gen_logs/memory.txt", "a") as file:
    #    file.write("\ndata during read call ------> = {}\n".format(data))
    return data
# Example usage:
#write_modify_data(1000,0b000100100011010001010110011110101010001001110011111111111111111111111111111111111111110010111010,3)
#write_modify_data(1000, 0b11111111111111111111111111111111,1)

#data = read_data_from_file(0x1000, 1)
#print(data)
#write_data_to_file(0x1004, 0xABCE)
#write_data_to_file(0x1008, 0xABCF)
#write_data_to_file(0x100a, 0xABCF)
#modify_data_in_file(0x1000, 0xFFFF)

#wddress = 1000
#wength = 2
#ata = read_data_from_file(address, length)
#rint(data)
#binary_string = ''.join(format(value, '016b') for value in data)
#print(binary_string)
