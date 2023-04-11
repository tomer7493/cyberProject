#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 2 - udp_local.py
# UDP client and server on localhost

import socket, sys
from threading import *
from zlib import decompress
import pygame
from queue import Queue

recv_q = Queue()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BUFSIZE = 655359
PORT_share_screen = 1060
width = 1900    
height = 1000

MAX_SIZE = 60000

def server(PORT_share_screen=1060):
    print ("server start run")
    app = pyg()
    app.start()
    s.bind(('127.0.0.1', PORT_share_screen))
    
    while(1):
        flag=0
        msg = b""
        #print("444")
        while(1):
            data, address = s.recvfrom(BUFSIZE)
            #collect msg parts
            part_nmb = int.from_bytes(data[0:2],'big')
            #print("000",part_nmb,len(data),len(data)-2)
            if part_nmb == 0:
                if flag ==1:
                    msg+=data[2:]
                else:
                    msg = data[2:]
                break
            else:
                msg+=data[2:]
                flag=1
                
        recv_q.put(msg)
        

def display(data):
    pixels = decompress(data)
    # Create the Surface from raw pixels
    img = pygame.image.fromstring(pixels, (width, height), 'RGB')
    picture = pygame.transform.scale(img, (width, height))
    # Display the picture
    screen.blit(picture, (0, 0))
    pygame.display.flip()
    # data = data.decode('ascii')
    # print ('The client at', address, 'says', repr(data))


class pyg(Thread):
    def __init__(self):
        Thread.__init__(self)
        

    def run(self):
        #print("py")
        counter = 0

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width, height))
       

        while True:
            clock.tick(50)  #wake 30 times in a second - every 33.3ms
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("bye")
                    sys.exit()

            if recv_q.empty() == False:
                data = recv_q.get()
                #print("111",counter, len(data),"\n")
                counter+=1
                if counter%200==0:
                    print (counter)
                try:
                    pixels = decompress(data)
                except:
                    print("we miss part of frame",counter)
                    continue
                #print("pyg" + len(data))
                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (width, height), 'RGB')
                picture = pygame.transform.scale(img, (width, height))
                # Display the picture
                screen.blit(picture, (0, 0))
                pygame.display.flip()

            
            pygame.display.update()    

        
            
            
# print ("server start run")
# app = pyg()
# app.start()
# server(PORT_share_screen)
