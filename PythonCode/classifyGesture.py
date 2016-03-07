#_________GestureRecognitionServiceCode(Need to insert into ServiceFramework)__________
import numpy as np

import readCom as rc
from ActiveFunctions import nonlin
from readDataFromFile import readWeights

GestureNum = 0
def classifyGesture():
    print(threading.currentThread().getName()+' On')#打印当前线程名
    #———————————加载分类器（权重矩阵）——————————————
    syn1, syn0=readWeights("weightsyn1.txt", "weightsyn0.txt")

    while True:
        print(threading.currentThread().getName()+' On')#打印当前线程名
        #___________________________Classifier_________________________
        #TODO：目前只有一个分类算法
        l0=SingleGroupData
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))
        Output=l2

        ##以下为将输出转为动作结果
        global GestureNum
        if Output<0.01:
            GestureNum=1
        else:
            GestureNum=0

        time.sleep(0.05)#为让线程不占用全部cpu