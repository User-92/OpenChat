import socket, select

def get_ip_port(path):
    with open(path, "r") as ipf:
        ipf_data = ipf.read()
        ipf.close()
    data_split = ipf_data.split(":")
    return [data_split[0],int(data_split[1])]

class Network():
    def __init__(self):
        self.ip, self.port = get_ip_port("server-ip.txt")
        self.addr = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.socket.connect(self.addr)
        except socket.error as e:
            print(e)
            
    def disconnect(self):
        self.socket.close()
        
n = Network()
n.connect()

BUFFER_SIZE = 2048
HEADER_SIZE = 5

while True:
    ins, outs, ex = select.select([n.socket], [], [], 0)
    for in_ in ins:
        data = ""
        recv_data = in_.recv(BUFFER_SIZE)
        if recv_data == b'':
            break
        message_length = int(recv_data[:HEADER_SIZE])
        data += recv_data.decode()
        while True:
            if len(data)-HEADER_SIZE >= message_length:
                if len(data)-HEADER_SIZE > message_length:
                    n.socket.setblocking(0)
                    while True:
                        try:
                            extra_data = in_.recv(BUFFER_SIZE)
                        except:
                            break
                    n.socket.setblocking(1)
                break
            recv_data = in_.recv(BUFFER_SIZE)
            data += recv_data.decode()
        data = data[HEADER_SIZE:message_length+HEADER_SIZE]
        
        print(data)
n.disconnect()