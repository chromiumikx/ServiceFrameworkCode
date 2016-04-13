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

import serial,time

OneFrame = []##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = []
readCom_StopFlag = False #TODO：此为串口读写线程退出的条件；添加：等待后续整理完决定
isReceive_Flag = False
def readCom(ComNumber="COM3",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        print(threading.currentThread().getName()+' On')#打印当前线程名
        global OneFrame,SingleGroupData
        global isReceive_Flag
        t0=time.clock()
        while True:
            # if time.clock()-t0 > 30:
            #     break
            if com.read(1)==b'h':
                testFrameStr=com.read(30)
                OneFrame=dataAnalysis(testFrameStr)
                ##每一帧都要进行阈值检测
                isReceive_Flag = isReceive(OneFrame)
                if isReceive_Flag:
                    print("Pass Gate",OneFrame)
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
import numpy

def isReceive(judgedFrame):
    canReceive = False
    AccGate = 150
    RotGate = None
    if sum([abs(i) for i in judgedFrame[:3]]) > 600:
        canReceive=True
    return canReceive

def dataAnalysis(OriginalData):
    #与下位机相对应，此处与TestDataTransfer对应
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
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名

    global SingleGroupData
    global isReceive_Flag
    while True:
        global GestureNum
        if isReceive_Flag:
            isReceive_Flag = False
            if OneFrame[2] > 0:
                GestureNum=1
            else:
                GestureNum=2
        time.sleep(0.05)#为让线程不占用全部cpu


#TODO:此处两个标记全局变量标记server与client连接开启情况；添加：待后续测试决定；
BreakCondition = False
Condition = False
import json as js


#TODO:此处两个标记全局变量标记server与client连接开启情况；添加：待后续测试决定；
BreakCondition = False
Condition = False
def socketDataServer(input_HOST='127.0.0.1', input_PORT=50033, input_backlog = 1):
    print(threading.currentThread().getName()+' On')#打印当前线程名
    global GestureNum, BreakCondition, Condition
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
    
    while True:
        conn,addr=s.accept()
        print ("Connected with "+addr[0]+':'+str(addr[1]))
        try:
            ##以下为指令处理模块，连接SDK中的API
            while True:
                RequireComm=conn.recv(1024).decode()
                if RequireComm == "Gesture":
                    conn.sendall((str(GestureNum)).encode())
                    GestureNum=0
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
                else:
                    #以下一句只是指接收到的命令不是“Gesture”时所做的处理，并非是说没接到指令
                    conn.sendall((" ").encode())

                print(threading.currentThread().getName()+' On')#打印当前线程名

                time.sleep(0.05)#为让线程不占用全部cpu

                if BreakCondition:
                    break        
            if Condition:
                break
        except:
            conn.close()
            pass

    s.close()

import matplotlib.pyplot as plt

def plotRealTime():
    pass

if __name__ == "__main__":
    #开锁保证串口读取完整
    lock=threading.Lock()
    tReadCom=threading.Thread(name="readCom",target=readCom)
    tClassifyGesture=threading.Thread(name="classify",target=classifyGesture)
    #tDataServer=threading.Thread(name="dataServer",target=socketDataServer)
    tPlot=threading.Thread(name="plotRealTime",target=plotRealTime)

    tReadCom.start()
    time.sleep(2)
    tClassifyGesture.start()
    time.sleep(2)
    #tDataServer.start()
    time.sleep(2)
    tPlot.start()

    print("Tag:运行子线程时是否会还运行主线程")

    tReadCom.join()
    tClassifyGesture.join()
    #tDataServer.join()
    tPlot.join()

    while True:
        time.sleep(0.01)
