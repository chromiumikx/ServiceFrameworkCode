import win32api
import win32con
import time

import GR_SDK
from VK_CODE import VK_CODE


print("Tag Open")
time.sleep(2)
try:
    myclient =GR_SDK.ClientConnect()
    while True:
        Num=""
        Num=myclient.getGesture()
        if Num == "4":
            win32api.keybd_event(32,0,0,0)  #空格键位码是32
            win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)

        if Num == "3":
            win32api.keybd_event(38,0,0,0)  #向上箭头键位码是38
            win32api.keybd_event(VK_CODE["up_arrow"],0,win32con.KEYEVENTF_KEYUP,0)

        if Num == "2":
            win32api.keybd_event(VK_CODE["F5"],0,0,0)  #空格键位码是32
            win32api.keybd_event(VK_CODE["F5"],0,win32con.KEYEVENTF_KEYUP,0)

        if Num == "1":
            win32api.keybd_event(VK_CODE["esc"],0,0,0)  #空格键位码是32
            win32api.keybd_event(VK_CODE["esc"],0,win32con.KEYEVENTF_KEYUP,0)
        
        time.sleep(0.02)
finally:
    myclient.stop()
