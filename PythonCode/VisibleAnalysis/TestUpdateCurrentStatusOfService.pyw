##____________________包含串口读取以及数据解析两个方法________________________
##
##注注注注：数据的帧设计可以不用“-”负号，使用多一位作为标志位，这样更容易处理，
##降低处理时间和性能消耗

##注意：不一定用符号“h”作为帧分解，转为十六进制传输后，
##可以以某个较大的十六进制数作为分解更简单
##
##注意：某些全局变量，为全局共享资源，如：
##      OneFrame
##      SingleGroupData
##      GestureNum
##      但最终只有某些线程会读取并清空他们

##TODO：合并到一个文件中并作整合，将三个子函数作为线程

import serial,time
import numpy as np

OneFrame = ([[0]*6])[0]##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = ([[0]*78])[0]
readCom_StopFlag = False #TODO：此为串口读写线程退出的条件；添加：等待后续整理完决定
isReceive_Flag = False
def readCom(ComNumber="COM5",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        global OneFrame,SingleGroupData,testFrameStr
        global isReceive_Flag
        
        t0 = time.clock()
        k = 0
        while True:
            if com.read(1)==b'h':
                testFrameStr=com.read(30)
                OneFrame=dataAnalysis(testFrameStr)
                ##每一帧都要进行阈值检测
                #isReceive_Flag = isReceive(OneFrame)
                if isReceive_Flag:
                    SingleGroupData = readOneGroup(GroupLen,com)

    finally:
        if com != None:
            com.close()

def readOneGroup(GroupLen,Com):
    ##此处必须使用while循环，因为不知何时遇上b'h'
    global OneFrame
    i=0
    OneGroupTemp=[]
    while True:
        if Com.read(1)==b'h':
            i=i+1
            OneFrameStr=Com.read(30)
            OneFrame=dataAnalysis(OneFrameStr)
            OneGroupTemp.extend(OneFrame)
        ##取13帧为一组数据，结果是是1*m维的数据
        if i == GroupLen:
            return OneGroupTemp

##—————————————阈值判决模块—————————————
##用于在接收一帧数据之前，判断这帧数据是否是有效动作，若有则接收13帧（待定）
##否则继续判决下一帧

def isReceive(judgedFrame):
    canReceive = False
    AccGate = 150
    RotGate = None
    if sum([abs(i) for i in judgedFrame[:3]]) > 600:
        canReceive=True
    return canReceive

def dataAnalysis(OriginalData):
    #与下位机相对应，此处与TestDataTransfer对应
    ##必须以增加位数优化处理方法。对齐数据使com.read()时取定长，否则需要一直同步，浪费时间
    Temp=(OriginalData.strip()).split()
    Data=[]
    for i in Temp:
        if i[0]==50:
            Data.append(int(i)-2000)
        elif i[0]==49:
            Data.append(1000-int(i))
    return Data

def saveData(Datas,Path,ActionType):
    #可以同时加上分类标记（待定），读取时便可以简单读取
    #一组数据（可能是一帧或13帧或其他）
    f=open(Path,"a")##以追加的方式写数据
    temp=[str(i)+" " for i in Datas]
    f.writelines(temp)
    f.write(str(ActionType)+" ")
    f.write("\n")
    f.close()

def judgeConnectedComnum():
    pass


##将收集标准数据的模块集成在这里，并在这里更改，不再独立成文件夹，后续将在此文件夹移进下位机代码
def readStandardData(ComNumber="COM5",GroupLen=13,GroupQuan=1,ActionType=1):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        global OneFrame,OneGroup
        isReceive_Flag = False
        j = 0
        while True:
            if com.read(1)==b'h':
                testFrameStr=com.read(30)
                OneFrame=dataAnalysis(testFrameStr)
                ##每一帧都要进行阈值检测
                isReceive_Flag = isReceive(OneFrame)
                if isReceive_Flag:
                    OneGroup = readOneGroup(GroupLen,com)
                    saveData(OneGroup,ActionType)
                    j = j+1
                    print("saved group %s"%(j))
                if j >= GroupQuan:
                    break
    finally:
        if com != None:
            com.close()

def saveData(Datas,ActionType):
    #可以同时加上分类标记（待定），读取时便可以简单读取
    #一组数据（可能是一帧或13帧或其他）
    f=open("data_%s.txt"%(ActionType),"a")##以追加的方式写数据
    temp=[str(i)+" " for i in Datas]
    f.writelines(temp)
    f.write(ActionType[-1]+" ")
    f.write("\n")
    f.close()


def collectTest():
    GroupQuan_ = 10
    while True:
        ActionType_ = input("输入动作类型（1.圆形  2.三角形 3.左滑动 4.右滑动 5.前缀“_”作为测试数据）：")
        if ActionType_ == "0":
            break
        readStandardData(GroupQuan=GroupQuan_,ActionType=ActionType_)

if __name__ == "__main__":
    import threading

    tReadCom=threading.Thread(name="readCom",target=readCom)
    tReadCom.start()
    time.sleep(1)


    ##界面————————显示系统实时运行状态，这部分可独立提取除去
    from tkinter import *
    root = Tk()
    root.iconbitmap('icon.ico')
    root.title("GR_Service running...")
    #root.overrideredirect(True)#窗口无边框
    root.attributes("-alpha", 0.8)#窗口透明度
    root.wm_attributes('-topmost',1)#窗口一直在最上
    root.geometry("300x45+0+0")                #是x 不是*
    root.resizable(width=True, height=True) #宽不可变, 高可变,默认为True

    version = Label(root, text="版本0.9", bd=1)
    version.grid(row=0, column=0,sticky=W)

    ConnectStatus = Label(root, text="连接状态：", bd=1)
    ConnectStatus.grid(row=1, column=0,sticky=W) 
    getConnectStatus = Label(root, text="Connecting", bd=1,anchor = 'w')
    getConnectStatus.grid(row=1, column=1) 

    currenAction = Label(root, text="实时数据：", bd=1)
    currenAction.grid(row=2, column=0,sticky=W) 
    getNowData = Label(root)
    getNowData.grid(row=2, column=1) #不能有sticky属性
    ##数据初始化
    time1 = ''
    testFrameStr = ''
    def tick_D():
        global time1,testFrameStr
        # 从运行程序的计算机上面获取当前的系统时间
        time2 = testFrameStr
        # 如果时间发生变化，代码自动更新显示的系统时间
        if time2 != time1:
            time1 = time2
            getNowData.config(text=time2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
        getNowData.after(200, tick_D)
    tick_D()

    currenAction = Label(root, text="实时动作：", bd=1)
    currenAction.grid(row=3, column=0,sticky=W) 
    getcurrenAction = Label(root,anchor = 'w')
    getcurrenAction.grid(row=3, column=1) #不能有sticky属性
    ##数据初始化
    time3 = ''
    GestureNumTemp = 0
    def tick_A():
        global time3,GestureNumTemp
        # 从运行程序的计算机上面获取当前的系统时间
        time4 = str(GestureNumTemp)
        # 如果时间发生变化，代码自动更新显示的系统时间
        if time4 != time3:
            time3 = time4
            getcurrenAction.config(text=time4)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
        getcurrenAction.after(200, tick_A)
    tick_A()

    ##程序退出按钮（叉按钮不行）
    def qiutScv():
        root.close()
        sys.exit(0)

    B = Button(root, text ="完全退出服务程序", command = qiutScv)
    B.grid(row=4, column=1)

    root.mainloop()
    ##界面————————显示系统实时状态


    tReadCom.join()


