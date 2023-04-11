#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 2 - udp_local.py
# UDP client and server on localhost

import socket
import mss
#import pygame
import sys
import random
from zlib import compress
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

BUFSIZE = 655359

WIDTH = 1900    
HEIGTH = 1000


def takeScreenshot():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGTH}
        img = sct.grab(monitor)
        pixels1 = compress(img.rgb, 6)
        return pixels1

def send_msg(data,address,PORT_share_screen):
    data_len = len(data)
    #print("111",data_len)
    MAX_SIZE = 60000
    l = len(data) // MAX_SIZE
    
    cnt=l-1
    start=0
    end  = MAX_SIZE-1
    if end > data_len:
        end = data_len
    for i in range(l+1):
        d = data[start:end]
        reverse_order = l-i
        part_nmb = reverse_order.to_bytes(2,'big') # convert int to two byes e.g. 4 will be b'\x00\x04'
        
        msg     = part_nmb+d
        
        print("222",part_nmb,start,end,end-start, len(msg))#from some reason ,if i put this in comment, it will stop work
        
        s.sendto(msg, (address, PORT_share_screen))
        start = end
        end+=MAX_SIZE-1
        if ( end > data_len):
            end = data_len
        

def client(stop,address = "127.0.0.1",PORT_share_screen = 1060):
    
    counter=0
    while stop.empty():
        
        msg = takeScreenshot()
        #print("\n000",counter,len(msg), type(msg))
        counter+=1
        if counter%200==0:
            print (counter)
        #s.sendto(msg, ('127.0.0.1', 1060))
        send_msg(msg,address,PORT_share_screen)
        time.sleep(0.03)


print ("client start")
# client()
