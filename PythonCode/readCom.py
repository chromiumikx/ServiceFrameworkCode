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
def readCom(ComNumber="COM3",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        t0=time.clock()
        j=0
        while True:
            i=0
            j=j+1
            OneGroupTemp=[]
            ##此处必须使用while循环，因为不知何时遇上b'h'
            while True:
                ch = com.read(1)
                if ch == b'h':
                    i=i+1
                    testFrameStr=com.read(30)
                    OneFrame=dataAnalysis(testFrameStr)
                    
                    if isReceive(OneFrame):
                        print(OneFrame)
                    OneGroupTemp.extend(OneFrame)
                ##取13帧为一组数据，结果是是1*m维的数据
                if i == GroupLen:
                    break
            SingleGroupData=OneGroupTemp
            ##测试时间控制，真正程序中删去
            if time.clock()-t0 > 20:
                break
    finally:
        if com != None:
            com.close()

##—————————————阈值判决模块—————————————
##用于在接收一帧数据之前，判断这帧数据是否是有效动作，若有则接收13帧（待定）
##否则继续判决下一帧
import numpy

def isReceive(judgedFrame):
    canReceive = False
    if sum(judgedFrame[:3]) > 25:
        canReceive=True
    return canReceive

def dataAnalysis(OriginalData):
    #与下位机相对应，此处与TestDataTransfer对应
    Temp=(OriginalData.strip()).split()
    Data=[]
    for i in range(len(Temp)):
        if Temp[i][0]==50:
            Data.append(int(Temp[i])-2000)
        elif Temp[i][0]==49:
            Data.append(1000-int(Temp[i]))
    return Data

def judgeConnectedComnum():
    pass

if __name__ == "__main__":
    readCom()
