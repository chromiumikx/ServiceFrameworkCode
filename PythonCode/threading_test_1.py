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


OneFrame = []##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = ([[0]*78])[0]
readCom_StopFlag = False #TODO：此为串口读写线程退出的条件；添加：等待后续整理完决定
isReceive_Flag = False
def readCom(ComNumber="COM3",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        global OneFrame,SingleGroupData
        global isReceive_Flag
        while True:
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
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #加载分类器（权重矩阵）
    syn0=readWeights("syn0.txt")
    ##扩展权重矩阵,可改变连接维数
    syn0_5 = []
    syn1=readWeights("syn1.txt")
    global SingleGroupData,GestureNum,isReceive_Flag
    while True:
        ##识别模块————1————
        ##识别此帧是否是简单手势，若是，不启动识别模块2，否则启动模块2
        GestureNum = isSimple(isReceive_Flag,OneFrame)
        ##下面这句阻断简单手势的识别
        if GestureNum == None:
            GestureNum = classifyModule_2(SingleGroupData,syn0,syn1)
        SingleGroupData = ([[0]*(len(SingleGroupData))])[0]##识别完毕后，将该组原始数据置零清除，取全展开

        if GestureNum == 1:
            print("IM 圆")
        if GestureNum == 2:
            print("IM 三角")
        if GestureNum == 3:
            print("——————》》》")
        if GestureNum == 4:
            print("《《《——————")

        time.sleep(0.01)#为让线程不占用全部cpu

        ##根据两个模块的识别结果给出最终的动作编号
        ##1.圆 2.三角形 3.左滑动 4.右滑动 5.前进 6.后退
        if True:
            pass

##识别模块————1————
##识别此帧是否是简单手势，若是，不启动识别模块2，否则启动模块2
def isSimple(isReceive_Flag_,SingleGroupData_):
    GestureNumTemp_1 = None
    ag = []
    for j in range(6):
        x = [SingleGroupData_[6*i+j] for i in range(int(len(SingleGroupData_)/6))]
        ag.append(x)

    if np.var(ag[0]) < 6000:
        if max(ag[1]) > 250 and np.mean(ag[0]) < 100 and np.mean(ag[2]) < 200:
            GestureNumTemp_1 = 3
        if max(ag[1]) < -250 and np.mean(ag[0]) < 100 and np.mean(ag[2]) < 200:
            GestureNumTemp_1 = 4
    return GestureNumTemp_1

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
    ##以下为将模块——1——的输出转为动作结果
    ##输出总共三位表示，可以一位一位的判断，以下以只判断第三位为例
    return GestureNum

def outputTrans(Output):
    a = []
    for i in range(len(Output)):
        if Output[i] > 0.5:
            a.append(1)
        else:
            a.append(0)
    return (4*a[0]+2*a[1]+a[2])

##识别模块————3————
##运用频域分析
def ByFFT(SingleGroupData_):
    ##若分类器-1输入为置零值，强制将输出转为0
    if SingleGroupData_ == ([[0]*(len(SingleGroupData_))])[0]:
        GestureNumTemp_3 = 0
    else:
        ay_f_11 = 0
        az_f_10 = 0
        gx_f_0 = 0
        gx_f_11 = 0
        gz_f_3 = 0
        gz_f_10 = 0
        fp = []
        GestureNumTemp_3 = 0
        for j in range(6):
            x = [SingleGroupData_[6*i+j]/10 for i in range(int(len(SingleGroupData_)/6))]
            x.extend([[0]*57][0])
            xf = np.fft.rfft(x)
            xf_ = 20*np.log10(np.clip(np.abs(xf),1e-20,1e100))
            fp.append(xf_[:15])
        ay_f_11 = fp[0][11]
        az_f_10 = fp[2][10]
        gx_f_0 = fp[3][0]
        gx_f_11 = fp[3][11]
        gz_f_3 = fp[5][3]
        gz_f_10 = fp[5][10]
        if FFTJudger(ay_f_11,az_f_10,gx_f_0,gx_f_11,gz_f_3,gz_f_10):
            GestureNumTemp_3 = 2
        else:
            GestureNumTemp_3 = 1
    return GestureNumTemp_3

def FFTJudger(ay_f_11,az_f_10,gx_f_0,gx_f_11,gz_f_3,gz_f_10):
    count=0
    if ay_f_11 > 39:
        count = count+1
    if az_f_10 > 37:
        count = count+1
    if gx_f_0 > 36:
        count = count+1
    if gx_f_11 > 36:
        count = count+1
    if gz_f_3 < 38:
        count = count+1
    if gz_f_10 > 43:
        count = count+1
    Result = True
    if count > 2:
        Result = False
    return Result


import json as js


#TODO:此处两个标记全局变量标记server与client连接开启情况；添加：待后续测试决定；
BreakCondition = False
Condition = False
def socketDataServer(input_HOST='127.0.0.1', input_PORT=50033, input_backlog = 1):
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
                elif RequireComm == "6Motions":
                    conn.sendall(js.dumps(OneFrame))
                    OneFrame=[[0]*6]
                else:
                    #以下一句只是指接收到的命令不是“Gesture”时所做的处理，并非是说没接到指令
                    conn.sendall((" ").encode())

                time.sleep(0.01)#为让线程不占用全部cpu

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
    tDataServer=threading.Thread(name="dataServer",target=socketDataServer)
    tPlot=threading.Thread(name="plotRealTime",target=plotRealTime)

    tReadCom.start()
    time.sleep(2)
    tClassifyGesture.start()
    time.sleep(2)
    tDataServer.start()
    time.sleep(2)
    tPlot.start()

    print("Tag:运行子线程时是否会还运行主线程")

    tReadCom.join()
    tClassifyGesture.join()
    tDataServer.join()
    tPlot.join()

    while True:
        time.sleep(0.01)
