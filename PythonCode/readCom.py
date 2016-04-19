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

OneFrame = []##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = ([[0]*78])[0]##初始化：要每个元素有实际数，不可用空列表代替
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
                    print(np.var([SingleGroupData[6*i] for i in range(int(len(SingleGroupData)/6))]))
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

def judgeConnectedComnum():
    pass


##将收集标准数据的模块集成在这里，并在这里更改，不再独立成文件夹，后续将在此文件夹移进下位机代码
def readStandardData(ComNumber="COM3",GroupLen=13,GroupQuan=1,ActionType=1):
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
                    print("Pass Gate",OneFrame)
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
    f.write(str(ActionType)+" ")
    f.write("\n")
    f.close()


def collectTest():
    GroupQuan_ = 10
    while True:
        ActionType_ = int(input("输入动作类型（1.圆形  2.三角形 3.左滑动 4.右滑动）："))
        if ActionType_ == 0:
            break
        readStandardData(GroupQuan=GroupQuan_,ActionType=ActionType_)

if __name__ == "__main__":
    readCom()
    #collectTest()
