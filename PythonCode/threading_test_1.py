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


SingleGroupData =[[0]*40]
readCom_StopFlag = False #TODO：此为串口读写线程退出的条件；添加：等待后续整理完决定
FrameperGroup=13
def readCom(ComNumber="COM3"):
    print(threading.currentThread().getName()+' On')#打印当前线程名
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        print(com.portstr)
        global SingleGroupData,readCom_StopFlag, FrameperGroup
        while True:
            ##以下两个为全局变量，储存串口读取的字符串和解析后的数据
            ##帧数同步
            #print(threading.currentThread().getName()+' On')#打印当前线程名
            try:
                lock.acquire()
                while True:
                    ch = com.read(1)
                    if ch == b'h':
                        break
                SingleGroupStr=com.read(10*FrameperGroup-1)#每帧数据由10个字符组成共13帧，预留一帧同步
                SingleGroupData=translateStr(SingleGroupStr)
                # if SingleGroupData !=[[0]*40]:
                #     print(SingleGroupData)
            finally:
                lock.release()
            ##TODO:以下为关闭串口读写的条件
            if readCom_StopFlag:
                break

            #time.sleep(0.05)
    finally:
        if com != None:
            com.close()

def chr3_2int(str_):
    int_=0
    sign=1
    for i in range(3):
        if str_[i]=='-':
            sign=-1
        else:
            int_=10*int_+int(str_[i])
    int_ = sign*int_
    return int_

#只能慢慢切片：
def translateStr(Str):
    global FrameperGroup
    Strs=str(Str,"utf-8")
    #每帧等分三分
    Temp=[]
    for i in range(FrameperGroup):
        for j in range(3):
            Temp.append(chr3_2int(Strs[j*3+i*10:j*3+3+i*10]))
    Temp.append(-1)
    return Temp


GestureNum = 0
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #———————————加载分类器（权重矩阵）——————————————
    syn1, syn0=readWeights("weightsyn1.txt", "weightsyn0.txt")

    while True:
        #print(threading.currentThread().getName()+' On')#打印当前线程名
        #___________________________Classifier_________________________
        #TODO：目前只有一个分类算法
        l0=SingleGroupData
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2

        ##以下为将输出转为动作结果:
        ##可以增加多层分类
        ##将分类结果直接编为数字字符
        global GestureNum
        if Output<0.01:
            GestureNum=1
        else:
            GestureNum=0

        #time.sleep(0.05)#为让线程不占用全部cpu

#TODO:此处两个标记全局变量标记server与client连接开启情况；添加：待后续测试决定；
BreakCondition = False
Condition = False
def socketDataServer(input_HOST='127.0.0.1', input_PORT=50033, input_backlog = 1):
    print(threading.currentThread().getName()+' On')#打印当前线程名
    global GestureNum, BreakCondition, Condition
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
            while True:
                RequireComm=conn.recv(1024).decode()
                if RequireComm == "Gesture":
                    #print("Get cmd of Gesture")
                    conn.sendall((str(GestureNum)).encode())
                else:
                    #以下一句只是指接收到的命令不是“Gesture”时所做的处理
                    conn.sendall(("NA").encode())

                #time.sleep(0.05)#为让线程不占用全部cpu

                if BreakCondition:
                    break        
            if Condition:
                break
        except:
            conn.close()
            pass

    s.close()


if __name__ == "__main__":
    #开锁保证串口读取完整
    lock=threading.Lock()
    tReadCom=threading.Thread(name="readCom",target=readCom)
    tClassifyGesture=threading.Thread(name="classify",target=classifyGesture)
    tDataServer=threading.Thread(name="dataServer",target=socketDataServer)

    tReadCom.start()
    time.sleep(2)
    tClassifyGesture.start()
    time.sleep(2)
    tDataServer.start()

    print("Tag:运行子线程时是否会还运行主线程")

    tReadCom.join()
    tDataServer.join()
    tClassifyGesture.join()

    while True:
        time.sleep(0.01)