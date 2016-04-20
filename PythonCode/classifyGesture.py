#_________GestureRecognitionServiceCode(Need to insert into ServiceFramework)__________
import numpy as np
import threading

import readCom as rc
from ActiveFunctions import nonlin
from readDataFromFile import *

GestureNum = 0
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #加载分类器（权重矩阵）
    syn0=readWeights("syn0.txt")
    ##扩展权重矩阵,可改变连接维数
    syn0_5 = []
    syn1=readWeights("syn1.txt")
    global OneFrame,SingleGroupData,GestureNum,isReceive_Flag,GestureNumTemp
    while True:
        GestureNum = classifyModule_2(SingleGroupData,syn0,syn1)
        SingleGroupData = ([[0]*(len(SingleGroupData))])[0]##识别完毕后，将该组原始数据置零清除，取全展开

        ##只要有动作，则缓存到GestureNumTemp中，以免被过快的识别流淹没
        if GestureNum != 0:
            GestureNumTemp = GestureNum

        if GestureNum == 1:
            print("IM 圆")
        if GestureNum == 2:
            print("IM 三角")
        if GestureNum == 3:
            print("《《《——————")
        if GestureNum == 4:
            print("——————》》》")

        time.sleep(0.01)#为让线程不占用全部cpu

        ##根据两个模块的识别结果给出最终的动作编号
        ##1.圆 2.三角形 3.左滑动 4.右滑动 #5.前进 6.后退
        if True:
            pass

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


##识别模块————1————
##识别此帧是否是简单手势，若是，不启动识别模块2，否则启动模块2
def isSimple(isReceive_Flag_,SingleGroupData_):
    GestureNumTemp_1 = 0
    global OneFrame
    if isReceive_Flag_:
        isReceive_Flag_ = False
        if OneFrame[2] > 0:
            GestureNumTemp_1=3#左滑动
        else:
            GestureNumTemp_1=4#右滑动
    return GestureNumTemp_1

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

if __name__=="__main__":
    pass
