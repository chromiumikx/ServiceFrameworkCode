import win32api
import win32con
import time

import GR_SDK


print("Tag Open")
time.sleep(10)
Condition=False
myclient =GR_SDK.ClientConnect()
t0=time.clock()
while True:
    Num=None
    Num=myclient.getGesture()
    if Num == "No Connect":
        print("No Connect")
        break
    if Num == "1":
        win32api.keybd_event(32,0,0,0)  #空格键位码是32
        win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)

    if Condition:
        time.sleep(10)
        win32api.keybd_event(38,0,0,0)  #向上箭头键位码是38
        win32api.keybd_event(38,0,win32con.KEYEVENTF_KEYUP,0)
    
    time.sleep(0.05)