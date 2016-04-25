import sys    
from tkinter import *
import time
def tick():
    global time1
    # 从运行程序的计算机上面获取当前的系统时间
    time2 = time.strftime('%H:%M:%S')
    # 如果时间发生变化，代码自动更新显示的系统时间
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
    clock.after(200, tick)
root = Tk()
root.iconbitmap('icon.ico')
root.title("GR_Service running...")
#root.overrideredirect(True)
root.attributes("-alpha", 0.8)#窗口透明度
root.wm_attributes('-topmost',1)#窗口一直在最上
root.geometry("300x45+0+0")                #是x 不是*
root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
time1 = ''
status = Label(root, text="版本0.9", bd=1)
status.grid(row=0, column=0,sticky=W)
currenAction = Label(root, text="实时动作：", bd=1)
currenAction.grid(row=1, column=0,sticky=W) 
clock = Label(root)
clock.grid(row=1, column=1) 
tick()
root.mainloop()
