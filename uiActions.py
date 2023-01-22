import uiFile
import PyQt5.QtWidgets
import sys

def buttons_actions (sendFile,lock,startShareScreen,stopShareScreen,turnOffStudentPC,turnStudentPCOn,unlock,watchStudentScreen,selectAllUsers,usersList):
    startShareScreen.clicked.connect(startShareScreenMet)

def startShareScreenMet():
    print(111)

