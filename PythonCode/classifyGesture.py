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
    global SingleGroupData,GestureNum,isReceive_Flag
    while True:
        print(threading.currentThread().getName()+' On')#打印当前线程名
        #___________________________Classifier_________________________
        ##识别模块————1————
        l0=SingleGroupData
        SingleGroupData = ([[0]*len(l0)])[0]##取完数后，将其置零，取全展开

        ##增补算法所需阈值元素（-1）
        l0.extend(-1)
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2
        ##以下为将模块——1——的输出转为动作结果
        ##输出总共三位表示，可以一位一位的判断，以下以只判断第三位为例
        GestureNumTemp_1=outputTrans(Output)

        zeros=([[0]*(len(l0)-1)])[0]
        ##若分类器-1输入为置零值，强制将输出转为0
        if l0[:-1] == zeros:
            GestureNumTemp_1=0
        if GestureNumTemp_1 == 1:
            print("IM 圆")
        if GestureNumTemp_1 == 2:
            print("三角》》》》》》》》》》》》》")
        
        SingleGroupData = zeros##取完数后，将其置零，取全展开

        ##识别模块————2————
        ##识别此帧是否是左右划东的手势
        if isReceive_Flag:
            isReceive_Flag = False
            if OneFrame[2] > 0:
                GestureNumTemp_2=1#左滑动
            else:
                GestureNumTemp_2=2#右滑动

        ##根据两个模块的识别结果给出最终的动作编号：
        if Condition:
            pass

        time.sleep(0.05)#为让线程不占用全部cpu

def outputTrans(Output):
    a = []
    for i in range(len(Output)):
        if Output[i] > 0.5:
            a.append(1)
        else:
            a.append(0)
    return (4*a[0]+2*a[1]+a[2])

if __name__=="__main__":
    SingleGroupData=((openFilegetData("data0.txt"))[0])[1]
    classifyGesture()
