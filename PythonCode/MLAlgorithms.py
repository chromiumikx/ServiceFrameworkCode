#coding:utf-8
import numpy as np
from readDataFromFile import openFilegetData
from ActiveFunctions import nonlin

def trainNeuralNetwork(PathList):
    #_________________数据与代码同一目录时用下列代码_________________________
    data=[]
    ##加载了三组标准输入数据，为一次性代码
    for P in PathList:
        data=data+(openFilegetData(P))

    ##快速生成标准输出矩阵（即分类标记）
    StandardOutput=[[0,0,0]]*21
    StandardOutput[0:7]=[[0,0,1]]*7

    x=np.array(data)
    y=np.array(StandardOutput)

    np.random.seed(1)

    #整个学习网络由两个（可修改成其他深度）权重矩阵（主要）构成，
    #syn0维数是40*40，syn1是40*3
    InputPoints=40
    InnerLayerPoints=40
    OutputPoints=3
    syn0=2*np.random.random((InputPoints,InnerLayerPoints))-1
    syn1=2*np.random.random((InnerLayerPoints,OutputPoints))-1

    for j in range(60000):
        #正常计算网络各层各节点的值
        l0=x
        l1=nonlin(np.dot(l0,syn0))
        l2=nonlin(np.dot(l1,syn1))

        #从后向前计算每层误差以及高确信误差
        #前层的误差由后层的高确信误差、该层与后层的权重网络决定
        l2_error=y-l2

        #以下是输出误差提示
        if(j%10000)==0:
            print("Error"+str(np.mean(np.abs(l2_error))))

        l2_delta=l2_error*nonlin(l2,deriv=True)

        l1_error=l2_delta.dot(syn1.T)

        l1_delta=l1_error*nonlin(l1,True)

        syn1+=l1.T.dot(l2_delta)
        syn0+=l0.T.dot(l1_delta)

    writefile0 = open("weightsyn0.txt", "w")
    for i in range(40):
        for j in range(40):
            writefile0.write(str(syn0[i][j])+" ")
        writefile0.write("\n")
    writefile0.close()

    writefile1 = open("weightsyn1.txt", "w")
    for i in range(40):
        for j in range(3):
            writefile1.write(str(syn1[i][j])+" ")
        writefile1.write("\n")
    writefile1.close()
    
    print(l2)
    return (syn0,syn1)


if __name__=="__main__":
    trainNeuralNetwork(["Circle.txt","UpDown.txt","LeftRight.txt"])
