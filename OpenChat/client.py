import socket, select, time, sys, pygame
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()

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
            
    def send(self, data):
        try:
            self.socket.sendall((f"{len(data):<{HEADER_SIZE}}"+data).encode())
        except Exception as e:
            print(f"Error: {e}")
            
    def disconnect(self):
        self.socket.close()
        
pygame.display.set_caption("OpenChat")
screen = pygame.display.set_mode((500,500))

# FONTS
title_font = pygame.font.SysFont(None, 36)
title_text = title_font.render('OpenChat Testing Chat Room', True, (255,255,255))
title_rect = pygame.Rect(0,0,500,70)
message_font = pygame.font.SysFont(None, 16)
        
n = Network()
n.connect()

BUFFER_SIZE = 2048
HEADER_SIZE = 5

messages = []
full_message = ""
enter_message_text = message_font.render("Enter A Message --> ", True, (255,255,255))

while True:
    screen.fill((0,0,0))
    
    pygame.draw.rect(screen, (60,60,60), title_rect)
    screen.blit(title_text, (70, 20))
    screen.blit(enter_message_text, (10, 474))
    
    m_offset = 0
    for message in messages:
        screen.blit(message, (10,450-m_offset))
        m_offset += 22
    
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
        
        messages.insert(0, message_font.render(data, True, (255,255,255)))
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == TEXTINPUT:
            full_message += event.text
            enter_message_text = message_font.render(f"Enter A Message --> {full_message}", True, (255,255,255))
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                n.send(full_message)
                full_message = ""
                enter_message_text = message_font.render("Enter A Message --> ", True, (255,255,255))
            if event.key == K_BACKSPACE:
                full_message = full_message[:-1]
                enter_message_text = message_font.render(f"Enter A Message --> {full_message}", True, (255,255,255))
            
    pygame.display.update()
    clock.tick(60)
        
    
n.disconnect()