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
selected_users = []


def buttons_actions(sendFile, lock, startShareScreen, stopShareScreen, turnOffStudentPC, turnStudentPCOn, unlock, watchStudentScreen, selectAllUsers, usersList, server):
    global running_server
    running_server = server

    startShareScreen.clicked.connect(startShareScreenMet)
    stopShareScreen.clicked.connect(stopShareScreenMet)
    usersList.itemSelectionChanged.connect(
        lambda: selected_users_into_list(usersList))


def startShareScreenMet():
    running_server.server_assignment_queue.put(
        ("startShareScreenMet", "", selected_users))
    print(111)


def stopShareScreenMet():
    running_server.server_assignment_queue.put(("stopShareScreenMet", "",""))
    print(111)


def selected_users_into_list(users_list):
    global selected_users
    for user_num in range(users_list.count()):
        if (users_list.item(user_num).isSelected()):
            selected_users.append(users_list.item(user_num))


def all_users_into_list(users_list):
    global selected_users
    for user_num in range(users_list.count()):
            selected_users.append(users_list.item(user_num))
