from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

global running_server
global selected_users
selected_users = []
global all_users
global is_all_users_selected
is_all_users_selected = False


def buttons_actions(
    lock,
    startShareScreen,
    stopShareScreen,
    unlock,
    watchStudentScreen,
    selectAllUsers,
    usersList,
    server,
):
    global running_server
    running_server = server

    global all_users
    all_users = usersList

    startShareScreen.clicked.connect(startShareScreenMet)
    stopShareScreen.clicked.connect(stopShareScreenMet)
    watchStudentScreen.clicked.connect(watchStudentScreenMet)

    lock.clicked.connect(lock_screen)
    unlock.clicked.connect(unlock_screen)

    selectAllUsers.clicked.connect(select_all_users)

    usersList.itemSelectionChanged.connect(lambda: selected_users_into_list(usersList))


def lock_screen():
    running_server.server_assignment_queue.put(("lock screen", "", selected_users))


def unlock_screen():
    running_server.server_assignment_queue.put(("unlock screen", "", selected_users))


def select_all_users():
    global is_all_users_selected
    is_all_users_selected = not is_all_users_selected
    print("working!!!")


def startShareScreenMet():
    running_server.server_assignment_queue.put(
        ("startShareScreenMet", "", selected_users)
    )


def stopShareScreenMet():
    running_server.server_assignment_queue.put(
        ("stopShareScreenMet", "", selected_users)
    )


def watchStudentScreenMet():
    running_server.server_assignment_queue.put(
        ("watchStudentScreenMet", "", selected_users)
    )


def add_user_to_list(username: str):
    all_users.addItem(username)


def selected_users_into_list(users_list):
    global selected_users
    selected_users = []
    if not is_all_users_selected:
        for user_num in range(users_list.count()):
            if users_list.item(user_num).isSelected():
                user_name = users_list.item(user_num).text()
                user_addr = running_server.database.get_user_by_single_info(user_name, 1)
                selected_users.append((user_addr[2], user_addr[3]))
    else:
        all_users_into_list(users_list)

def all_users_into_list(users_list):
    global selected_users
    selected_users = []
    for user_num in range(users_list.count()):
        selected_users.append(users_list.item(user_num))
