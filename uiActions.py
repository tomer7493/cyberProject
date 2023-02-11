import uiFile
import PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

global running_server
global selected_users

def buttons_actions (sendFile,lock,startShareScreen,stopShareScreen,turnOffStudentPC,turnStudentPCOn,unlock,watchStudentScreen,selectAllUsers,usersList,server):
    global running_server 
    running_server = server
    
    startShareScreen.clicked.connect(startShareScreenMet)
    stopShareScreen.clicked.connect(stopShareScreenMet)
    usersList.itemSelectionChanged.connect(lambda: users_list_met(usersList))

def startShareScreenMet():
    running_server.assignment_queue.put(("startShareScreenMet",selected_users))
    print(111)
    
def stopShareScreenMet():
    running_server.assignment_queue.put(("stopShareScreenMet",""))
    print(111)

def users_list_met(users_list):
    global selected_users
    selected_users = []
    for user_num in range(users_list.count()):
        if (users_list.item(user_num).isSelected()):
            selected_users.append(users_list.item(user_num))
    # for user_num in users_list.items():
        # if (user.isSelected()):
            # selected_users.append(user)
            


    


