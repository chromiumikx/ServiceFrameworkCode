##________________________Gesture Recognition Services Component_____________________________
##主要代码从threading_test_1移植过来
# -*- coding: UTF8 -*-
#测试 两个线程一读一取同一变量
#当增加到3个线程时，有可能堵塞，使socketsenddata线程不能及时发送最新数据
#所以后续测试若实时性不够，应将读取串口和处理放在同一线程

import serial
import numpy as np
import sys
import socket
import time
import threading

from ActiveFunctions import nonlin
from readDataFromFile import readWeights


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


testFrameStr = ''
OneFrame = ([[0]*6])[0]##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = ([[0]*78])[0]
isReceive_Flag = False
readComQuitedFlag = False
def readCom(ComNumber="COM5",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        global OneFrame,SingleGroupData,testFrameStr
        global isReceive_Flag,SafeQuitFlag,readComQuitedFlag
        while True:
            if com.read(1)==b'h':
                testFrameStr=com.read(30)
                OneFrame=dataAnalysis(testFrameStr)
                ##每一帧都要进行阈值检测
                isReceive_Flag = isReceive(OneFrame)
                if isReceive_Flag:
                    SingleGroupData = readOneGroup(GroupLen,com)

            if SafeQuitFlag:
                break
    finally:
        if com != None:
            com.close()
        readComQuitedFlag = True
        print("readCom Quit\n")

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




GestureNum = 0
classifyQuitedFlag = False
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #加载分类器（权重矩阵）
    syn0=readWeights("syn0.txt")
    ##扩展权重矩阵,可改变连接维数
    syn0_5 = []
    syn1=readWeights("syn1.txt")
    global OneFrame,SingleGroupData,GestureNum
    global isReceive_Flag,GestureNumTemp,GestureNumTemp_forUI
    global SafeQuitFlag,classifyQuitedFlag
    while True:
        GestureNum = classifyModule_2(SingleGroupData,syn0,syn1)
        SingleGroupData = ([[0]*(len(SingleGroupData))])[0]##识别完毕后，将该组原始数据置零清除，取全展开

        ##只要有动作，则缓存到GestureNumTemp中，以免被过快的识别流淹没
        if GestureNum != 0:
            GestureNumTemp = GestureNum
            GestureNumTemp_forUI = GestureNum

        if GestureNum == 1:
            print("IM 圆")
        if GestureNum == 2:
            print("IM 三角")
        if GestureNum == 3:
            print("《《《——————")
        if GestureNum == 4:
            print("——————》》》")

        time.sleep(0.01)#为让线程不占用全部cpu

        if SafeQuitFlag:
            break
    classifyQuitedFlag = True
    print("classify Quit\n")

##识别模块————2————
def classifyModule_2(SingleGroupData_,syn0,syn1):
    ##若分类器-1输入为置零值，强制将输出转为0
    if SingleGroupData_ == ([[0]*(len(SingleGroupData_))])[0]:
        GestureNum = 0
    else:
        l0=SingleGroupData_[:]

        ##增补算法所需阈值元素（-1）
        l0.append(-1)
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2
        GestureNum = outputTrans(Output)
    return GestureNum

##以下为将模块——1——的输出转为动作结果
##输出总共三位表示，可以一位一位的判断，以下以只判断第三位为例
def outputTrans(Output):
    a = []
    for i in range(len(Output)):
        if Output[i] > 0.5:
            a.append(1)
        else:
            a.append(0)
    return (4*a[0]+2*a[1]+a[2])


import json as js



##动作缓存
GestureNumTemp = 0
socketQuitedFlag = False
def socketDataServer(input_HOST='127.0.0.1', input_PORT=50011, input_backlog = 2):
    global GestureNum, BreakCondition, Condition,GestureNumTemp
    ##以下为 为API提供全局资源，供用户读取
    global OneFrame
    HOST=input_HOST
    PORT=input_PORT
    backlog = input_backlog
    
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print ("Failed to create socket")
        sys.exit()
    print ("Server_Socket Created")
    
    try:
        s.bind((HOST,PORT))
    except socket.error as msg:
        s.close()
        print ('Bind failed. Error Code:'+str(msg[0])+' Message '+str(msg[1]))
        sys.exit()
    print ("Socket bind complete")
    
    s.listen(backlog)
    print ("Socket is now listening")

    global SafeQuitFlag,socketQuitedFlag
    while True:
        conn,addr=s.accept()
        print("显示则不阻塞")
        print ("Connected with "+addr[0]+':'+str(addr[1]))
        try:
            ##以下为指令处理模块，连接SDK中的API
            while True:
                RequireComm=conn.recv(1024).decode()
                if RequireComm == "Gesture":
                    conn.sendall((str(GestureNumTemp)).encode())
                    GestureNumTemp=0
                elif RequireComm == "Accs":
                    Accs=OneFrame[0:3]
                    ##还要将此list转成json或其他格式
                    conn.sendall(js.dumps(Accs))
                    OneFrame=[[0]*6]
                elif RequireComm == "Rots":
                    Rots=OneFrame[0:3]
                    ##还要将此list转成json或其他格式
                    conn.sendall(js.dumps(Rots))
                    OneFrame=[[0]*6]
                elif RequireComm == "6Motions":
                    conn.sendall(js.dumps(OneFrame))
                    OneFrame=[[0]*6]
                elif RequireComm == "close_socketDataServer":
                    break
                else:
                    #以下一句只是指接收到的命令不是“Gesture”时所做的处理
                    #并非是说没接到指令
                    conn.sendall((" ").encode())

                time.sleep(0.01)#为让线程不占用全部cpu

        except:
            conn.close()
            pass

        if SafeQuitFlag:
            break
    s.close()
    socketQuitedFlag = True
    print("socket Quit\n")

import matplotlib.pyplot as plt

def plotRealTime():
    pass

if __name__ == "__main__":
    SafeQuitFlag = False
    tReadCom=threading.Thread(name="readCom",target=readCom)
    tClassifyGesture=threading.Thread(name="classify",target=classifyGesture)
    tDataServer=threading.Thread(name="dataServer",target=socketDataServer)
    tPlot=threading.Thread(name="plotRealTime",target=plotRealTime)

    tReadCom.setDaemon(True)
    tClassifyGesture.setDaemon(True)
    tDataServer.setDaemon(True)
    tPlot.setDaemon(True)

    tReadCom.start()
    time.sleep(1)
    tClassifyGesture.start()
    time.sleep(1)
    tDataServer.start()
    time.sleep(1)
    tPlot.start()

    print("Tag:运行子线程时是否会还运行主线程")

    ##界面————————显示系统实时运行状态，这部分可独立提取除去
    from tkinter import *
    root = Tk()
    root.iconbitmap('icon.ico')
    root.title("GR_Service running...")
    #root.overrideredirect(True)#窗口无边框
    root.attributes("-alpha", 0.8)#窗口透明度
    root.wm_attributes('-topmost',1)#窗口一直在最上
    root.geometry("300x130+0+0")                #是x 不是*
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
        time2 = testFrameStr
        if time2 != time1:
            time1 = time2
            getNowData.config(text=time2)
        getNowData.after(200, tick_D)
    tick_D()

    currenAction = Label(root, text="实时动作：", bd=1)
    currenAction.grid(row=3, column=0,sticky=W) 
    getcurrenAction = Label(root,anchor = 'w')
    getcurrenAction.grid(row=3, column=1) #不能有sticky属性
    ##数据初始化
    time3 = ''
    GestureNumTemp_forUI = 0
    def tick_A():
        global time3,GestureNumTemp_forUI
        DictGesture = {"0":"无动作","1":"圆形","2":"三角形","3":"<<<左滑动","4":"右滑动>>>","5":"未定义动作","6":"未定义动作"}
        time4 = DictGesture[str(GestureNumTemp_forUI)]
        GestureNumTemp_forUI = 0
        if time4 != time3:
            time3 = time4
            getcurrenAction.config(text=time4)
        getcurrenAction.after(200, tick_A)
    tick_A()

    ##程序退出按钮（叉按钮不行）
    SafeQuitFlag = False
    def qiutScv():
        global SafeQuitFlag,readComQuitedFlag,classifyQuitedFlag,socketQuitedFlag
        SafeQuitFlag = True
        print("I'm Buttoned")
        ##以下处理socketAccept阻塞无法退出线程的情况
        host = '127.0.0.1'
        port = 50011
        StopTheSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        StopTheSocket.connect((host,port))
        StopTheSocket.sendall(("close_socketDataServer").encode())
        StopTheSocket.close()
        while readComQuitedFlag and  socketQuitedFlag:
            print("myself Quit")
            sys.exit(0)
            break
        root.destroy()

    B = Button(root, text ="完全退出服务程序", command = qiutScv)
    B.grid(row=4, column=1)

    root.mainloop()
    ##界面————————显示系统实时状态



    tReadCom.join()
    tClassifyGesture.join()
    tDataServer.join()
    tPlot.join()

    time.sleep(0.01)
