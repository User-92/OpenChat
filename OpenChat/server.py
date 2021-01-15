import socket, threading, json

def get_ip_port(path):
    with open(path, "r") as ipf:
        ipf_data = ipf.read()
        ipf.close()
    data_split = ipf_data.split(":")
    return [data_split[0],int(data_split[1])]
    
def send_data(data, conn):
    try:
        conn.sendall((f"{len(data):<{HEADER_SIZE}}"+data).encode())
    except Exception as e:
        print(f"Error: {e}")

ipport = get_ip_port("server-ip.txt")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(tuple(ipport))
s.listen(10)
bufsize = 2048

HEADER_SIZE = 5

def client_thread(conn,users):
    #send_data("Server >> Welcome To OpenChat's Testing Server!", conn)
    username = "UnknownUser"
        
    while True:
        try:
            data = ""
            recv_data = conn.recv(bufsize)
            if recv_data == b'':
                print("Someone disconnected")
                break
            message_length = int(recv_data[:HEADER_SIZE])
            data += recv_data.decode()
            while True:
                if len(data)-HEADER_SIZE >= message_length:
                    if len(data)-HEADER_SIZE > message_length:
                        n.socket.setblocking(0)
                        while True:
                            try:
                                extra_data = conn.recv(bufsize)
                            except:
                                break
                        n.socket.setblocking(1)
                    break
                recv_data = conn.recv(bufsize)
                data += recv_data.decode()
            data = data[HEADER_SIZE:message_length+HEADER_SIZE]
            
            if data:
                update_data = json.loads(data)
                update_keys = [key for key in update_data.keys()]
                for update_key in update_keys:
                    if update_key == "send_message":
                        for user in users:
                            if user == conn:
                                data_send = {"new_message":f"YOU > {update_data[update_key]}"}
                            else:
                                data_send = {"new_message":f"{username} >> {update_data[update_key]}"}
                            send_data(json.dumps(data_send), user)
                    if update_key == "username_update":
                        username = update_data[update_key]
                
        except Exception as e:
            print(e)
            break
            
    users.remove(conn)
    conn.close()

print("Server has started, waiting for connections.")
users = []

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    users.append(conn)
    
    c_thread = threading.Thread(target=client_thread, args=[conn,users])
    c_thread.start()