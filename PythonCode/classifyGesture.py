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
    syn1=readWeights("syn1.txt")
    global SingleGroupData
    while True:
        print(threading.currentThread().getName()+' On')#打印当前线程名
        #___________________________Classifier_________________________
        l0=SingleGroupData
        SingleGroupData =[[0]*len(l0)]##取完数后，将其置零

        ##增补算法所需阈值元素（-1）
        l0.append(-1)
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2
        print(Output)

        ##以下为将输出转为动作结果
        ##输出总共三位表示，可以一位一位的判断，以下以只判断第三位为例
        global GestureNum
        GestureNum=outputTrans(Output)

        time.sleep(0.05)#为让线程不占用全部cpu

def outputTrans(Output):
    pass

if __name__=="__main__":
    SingleGroupData=((openFilegetData("data0.txt"))[0])[1]
    classifyGesture()
