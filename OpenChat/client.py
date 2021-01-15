import socket, select, time, sys, pygame, json
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
screen = pygame.display.set_mode((900,600),pygame.RESIZABLE)

BUFFER_SIZE = 2048
HEADER_SIZE = 5

# FONTS
title_font = pygame.font.SysFont(None, 36)
title_text = title_font.render('OpenChat Testing Chat Room', True, (255,255,255))
title_rect = pygame.Rect(0,0,screen.get_width(),70)
message_font = pygame.font.SysFont(None, 19)

# Yes, I know the menu function has very very very bad code. I was just prototyping. I'll implement classes later

def menu():
    global screen
    enter_font = pygame.font.SysFont(None, 21)
    name_font = pygame.font.SysFont(None, 35)
    enter_name_text = enter_font.render("USERNAME", True, (142,146,151))
    login_text = enter_font.render("Login", True, (230,230,230))
    login_text_pos = [420,367]
    enter_name_text_pos = [243, 206]
    name_text_image_pos = []
    
    squ1 = pygame.Rect(150,150,600,300)
    name_square = pygame.Rect(246,230,400, 50)
    name_square_outline = pygame.Rect(243,227,406, 56)
    login_rect = pygame.Rect(271,350,350,50)
    
    name_text = ""
    name_text_image = None
    typing = False
    cursor_blink_time = 0
    cursor_rect = pygame.Rect(248,240,5,35)
    
    running = True
    
    while running:
        screen.fill((54,57,63))
        
        pygame.draw.rect(screen, (44,47,53), squ1)
        pygame.draw.rect(screen, (14,17,23), name_square_outline)
        pygame.draw.rect(screen, (34,37,43), name_square)
        pygame.draw.rect(screen, (114,137,218), login_rect)
        screen.blit(login_text, login_text_pos)
        screen.blit(enter_name_text, enter_name_text_pos)
        
        if typing:
            cursor_blink_time += 1
            if cursor_blink_time < 50:
                pygame.draw.rect(screen,(255,255,255), cursor_rect)
            elif cursor_blink_time > 100:
                cursor_blink_time = 0
                
        if name_text_image:
            screen.blit(name_text_image, (246,245))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == TEXTINPUT:
                if typing and not len(name_text) >= 15:
                    name_text += event.text
                    if name_text_image:
                        old_width = name_text_image.get_width()
                    else:
                        old_width = 0
                    name_text_image = name_font.render(name_text,True,(255,255,255))
                    cursor_rect.x += name_text_image.get_width() - old_width
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pass
                if event.key == K_BACKSPACE:
                    name_text = name_text[:-1]
                    
                    if name_text_image:
                        old_width = name_text_image.get_width()
                    else:
                        old_width = 0
                    name_text_image = name_font.render(name_text,True,(255,255,255))
                    cursor_rect.x += name_text_image.get_width() - old_width
                    
                    name_text_image = name_font.render(name_text,True,(255,255,255))
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx,my = pygame.mouse.get_pos()
                    if name_square.collidepoint((mx,my)):
                        typing = True
                    else:
                        typing = False
                        
                    if login_rect.collidepoint((mx,my)):
                        running = False
                        
            elif event.type == pygame.VIDEORESIZE:
                old_width = screen.get_width()
                old_height = screen.get_height()
                squ1 = pygame.Rect((event.w-squ1.width)//2, (event.h//2)-(squ1.height//2), squ1.width, squ1.height)
                name_square = pygame.Rect(name_square.x+(event.w-old_width)//2,name_square.y+(event.h-old_height)//2,400, 50)
                name_square_outline = pygame.Rect(name_square.x-3,name_square.y-3,name_square.width+6,name_square.height+6)
                login_rect = pygame.Rect(login_rect.x+(event.w-old_width)//2,login_rect.y+(event.h-old_height)//2,login_rect.width,login_rect.height)
                cursor_rect = pygame.Rect(cursor_rect.x+(event.w-old_width)//2,cursor_rect.y+(event.h-old_height)//2,cursor_rect.width,cursor_rect.height)
                login_text_pos = [login_text_pos[0]+(event.w-old_width)//2,login_text_pos[1]+(event.h-old_height)//2]
                enter_name_text_pos = [enter_name_text_pos[0]+(event.w-old_width)//2, enter_name_text_pos[1]+(event.h-old_height)//2]
                
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                    
        pygame.display.update()
        clock.tick(60)
    return name_text
    
username = menu()
        
n = Network()
n.connect()

send_data = {"username_update":username}
n.send(json.dumps(send_data))

messages = []
full_message = ""
enter_message_text = message_font.render("Enter A Message --> ", True, (255,255,255))

while True:
    screen.fill((54,57,63))
    
    pygame.draw.rect(screen, (47,49,54), title_rect)
    screen.blit(title_text, ((screen.get_width()-title_text.get_width())//2, 20))
    screen.blit(enter_message_text, (10, screen.get_height()-26))
    
    m_offset = 0
    for message in messages:
        screen.blit(message, (10,(screen.get_height()-m_offset)-50))
        m_offset += message_font.get_height()+6
    
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
        
        if data:
            socket_event = json.loads(data)
            event_types = [key for key in socket_event.keys()]
        for event_type in event_types:
            data_list = socket_event[event_type]
            print(data_list)
            if event_type == "new_message":
                messages.insert(0, message_font.render(data_list, True, (255,255,255)))
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == TEXTINPUT:
            full_message += event.text
            enter_message_text = message_font.render(f"Enter A Message --> {full_message}", True, (255,255,255))
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                send_data = {"send_message":full_message}
                n.send(json.dumps(send_data))
                full_message = ""
                enter_message_text = message_font.render("Enter A Message --> ", True, (255,255,255))
            if event.key == K_BACKSPACE:
                full_message = full_message[:-1]
                enter_message_text = message_font.render(f"Enter A Message --> {full_message}", True, (255,255,255))
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            title_rect = pygame.Rect(0,0,event.w,70)

            
    pygame.display.update()
    clock.tick(60)
        
    
n.disconnect()