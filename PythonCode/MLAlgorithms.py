#coding:utf-8
import numpy as np
from readDataFromFile import openFilegetData
from ActiveFunctions import nonlin
from pylab import arange, plt
from drawnow import drawnow

def trainNeuralNetwork(PathList=["data_1.txt","data_2.txt"]):
    #_________________数据与代码同一目录时用下列代码_________________________
    PathsData=[]
    PathsTags=[]
    ##加载了三组标准输入数据，并增加算法所需（-1）阈值元素，为一次性代码
    for P in PathList:
        Temp=openFilegetData(P)
        for i in range(len(Temp[0])):
            Temp[0][i].append(-1)
        PathsData.extend(Temp[0])
        ##所有的标记（未转化为多维），全列成一列
        PathsTags.extend(Temp[1])

    ##快速生成标准输出矩阵（即分类标记）
    StandardOutput=[]
    ##通过列表生成器，用数组替换每一个元素将其变为二维数组，例如用[0,0,1]代替pathtags中的1元素
    StandardOutput=[dimTrans(i) for i in PathsTags]

    x=np.array(PathsData)
    y=np.array(StandardOutput)

    np.random.seed(1)

    #整个学习网络由两个（可修改成其他深度）权重矩阵（主要）构成，
    #syn0维数是40*40，syn1是40*3
    InputPoints=79
    InnerLayerPoints=79
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

        syn1 = syn1+l1.T.dot(l2_delta)/100
        syn0 =syn0+l0.T.dot(l1_delta)/100

    saveWeights(syn0,"syn0")
    saveWeights(syn1,"syn1")
    print(l2)
    
    return (syn0,syn1)

def dimTrans(Dim1):
    ##通过列表生成器，例如用[-1,-1,1]代替pathtags中的1元素
    if Dim1 > 7 or Dim1 < 0:
        return [0,0,0]
    temp = list(bin(Dim1))
    temp[temp.index('b')] = '0'
    DimN = [converI(i) for i in temp[-3:]]
    
    return DimN

def converI(i):
    if i=='0':
        return -1+0.00000001
    if i=='1':
        return 1-0.00000001

def saveWeights(WeightsVars,FileNmae):
    writefile = open((FileNmae+".txt"), "w")
    for i in WeightsVars:
        for j in i:
            writefile.write(str(j)+" ")
        writefile.write("\n")
    writefile.close()


def testFFT():
    ##注意：共六个变量，每个变量有一定数量的频点，找出差别最大的频点Ki，识别时只要有一定数量的K点即可认为区分开了
    import matplotlib.pyplot as plt
    Data_1,tags_1 = openFilegetData("data_1.txt")
    #Data_2,tags_2 = openFilegetData("data_2.txt")

    ay_f_11 = 0
    az_f_10 = 0
    gx_f_0 = 0
    gx_f_11 = 0
    gz_f_3 = 0
    gz_f_10 = 0
    Judge_tags_1 = []
    for k in Data_1:
        fp = []
        for j in range(6):
            x = [k[6*i+j]/10 for i in range(int(len(k)/6))]
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
        result = FFTJudger(ay_f_11,az_f_10,gx_f_0,gx_f_11,gz_f_3,gz_f_10)
        Judge_tags_1.append(result)
    print(Judge_tags_1)
    print((len(Data_1)-sum([tags_1[i]-Judge_tags_1[i] for i in range(len(tags_1))]))/len(Data_1))


def ByFFT():
    pass

##判断模块
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
    Result = 0
    if count > 2:
        Result = 1
    return Result

def isSimple():
    pass

if __name__=="__main__":
    #trainNeuralNetwork()
    isSimple()
