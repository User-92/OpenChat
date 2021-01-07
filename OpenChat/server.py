import socket, threading

def get_ip_port(path):
    with open(path, "r") as ipf:
        ipf_data = ipf.read()
        ipf.close()
    data_split = ipf_data.split(":")
    return [data_split[0],int(data_split[1])]

ipport = get_ip_port("server-ip.txt")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(tuple(ipport))
s.listen(10)
bufsize = 2048

HEADER_SIZE = 5

def client_thread(conn):
    try:
        #print(json.dumps(update).encode())
        send_data = "#####################################\nWelcome To OpenChat's Testing Server!\n#####################################\n"
        conn.sendall((f"{len(send_data):<{HEADER_SIZE}}"+send_data).encode())
    except Exception as e:
        print(f"Error: {e}")
    conn.close()
        #try:
        #    data = ""
        #    recv_data = in_.recv(BUFFER_SIZE)
        #    message_length = int(recv_data[:HEADER_SIZE])
        #    data += recv_data.decode()
        #    while True:
        #        if len(data)-HEADER_SIZE >= message_length:
        #            if len(data)-HEADER_SIZE > message_length:
        #                n.socket.setblocking(0)
        #                while True:
        #                    try:
        #                        extra_data = in_.recv(BUFFER_SIZE)
        #                    except:
        #                        break
        #                n.socket.setblocking(1)
        #            break
        #        recv_data = in_.recv(BUFFER_SIZE)
        #        data += recv_data.decode()
        #    data = data[HEADER_SIZE:message_length+HEADER_SIZE]
        #    
        #    if data:
        #        print(data)
        #        
        #except Exception as e:
        #    print(e)
        #    break
        

print("Server has started, waiting for connections.")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    
    c_thread = threading.Thread(target=client_thread, args=[conn])
    c_thread.start()