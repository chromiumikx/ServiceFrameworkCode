#_________GestureRecognitionServiceCode(Need to insert into ServiceFramework)__________
import numpy as np

import readCom as rc
from ActiveFunctions import nonlin
from readDataFromFile import readWeights

GestureNum = 0
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #———————————加载分类器（权重矩阵）——————————————
    [syn0, syn1]=readWeights(["weightsyn0.txt", "weightsyn1.txt"])

    while True:
        print(threading.currentThread().getName()+' On')#打印当前线程名
        #___________________________Classifier_________________________
        l0=SingleGroupData
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2

        ##以下为将输出转为动作结果
        ##输出总共三位表示，可以一位一位的判断，以下以只判断第三位为例
        global GestureNum
        if Output[2]0.5:
            GestureNum=1
        else:
            GestureNum=0

        time.sleep(0.05)#为让线程不占用全部cpu