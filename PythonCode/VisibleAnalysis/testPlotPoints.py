import serial
import time
import threading
import matplotlib.pyplot as plt

from ActiveFunctions import nonlin


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

OneFrame = [0*i for i in range(100)]##三个加速度三个角速度，已解码，供后续API制作使用
SingleGroupData = []
def readCom(ComNumber="COM3",GroupLen=13):
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        global OneFrame,SingleGroupData
        global isReceive_Flag
        t0=time.clock()

        while True:
            if com.read(1)==b'h':
                testFrameStr=com.read(30)
                OneFrame=dataAnalysis(testFrameStr)
            time.sleep(0.01)

    finally:
        if com != None:
            com.close()

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

def Loop():
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x=[i for i in range(100)]
    y=[0*i for i in range(100)]
    line1, = ax.plot(x, y)
    plt.ylim(-400, 400)
    global OneFrame
    while True:
        y.pop(0)
        y.append(OneFrame[1])
        line1.set_ydata(y)
        # to refresh the figure by force
        fig.canvas.draw()
        time.sleep(0.01)

if __name__=="__main__":
    trd=threading.Thread(target=readCom)
    tLp=threading.Thread(target=Loop)
    trd.start()
    tLp.start()
    print(threading.currentThread().getName()+' On')#打印当前线程名
    tLp.join()
    trd.join()
