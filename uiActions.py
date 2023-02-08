import uiFile
import PyQt5.QtWidgets
import sys
import server

def buttons_actions (sendFile,lock,startShareScreen,stopShareScreen,turnOffStudentPC,turnStudentPCOn,unlock,watchStudentScreen,selectAllUsers,usersList):
    startShareScreen.clicked.connect(startShareScreenMet)

def startShareScreenMet():
    print(111)

#returns the variable name of specific variable
def get_var_name(variable):
    globals_dict = globals()
    #server.Server.
    server.assignment_queue.put( [var_name for var_name in globals_dict if globals_dict[var_name] is variable])


