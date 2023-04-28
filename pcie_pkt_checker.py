import random
class PktBase:
    def __init__(self):
       self.bdf = 5
       self.cfg_type = 0
       self.ep = 0
       self.td = 0
       self.block = 1

    def pkt_rand(self):
        self.bdf = random.randint(0, 2**8 - 1)
        self.cfg_type = random.randint(0, 1)
        self.ep = random.randint(0, 1)
        self.td = random.randint(0, 1)
        self.block = 1

    def pkt_rand_def(self):
        print('bdf value is {}, cfg_type is {}, ep is {}, block is {}'.format(self.bdf, self.cfg_type, self.ep, self.block))

    def generate_packets(num_packets):
        packets = []
        for i in range(num_packets):
            p = PktBase()
            p.pkt_rand()
            packets.append(p)
        return packets

    def check_packets(packets):
        for i, p in enumerate(packets):
            if not (0 <= p.bdf < 2**8 and 0 <= p.cfg_type <= 1 and 0 <= p.ep <= 1 and 0 <= p.td <= 1 and p.block == 1):
                print("Packet {} is invalid".format(i))
        return False
        return True

num_packets = 10
pkt = PktBase()
packets = pkt.generate_packets(num_packets)
print("Generated {} packets:".format(num_packets))
for p in packets:
    p.pkt_rand_def()

    
if check_packets(packets):
    print("All packets are valid")
else:
    print("Error: invalid packet generated")

