#-*- coding: UTF-8 -*-
#________________________________读取文件数据____________________________________
#______________________________读取标准输入文件__________________________________

def openFilegetData(Path="data0.txt"):
    f=open(Path,"r")
    temp=f.readlines()
    dataread=[]
    tags=[]
    for i in range(len(temp)):
        dataread.append([int(k) for k in ((temp[i].strip()).split())])
        tags.append(dataread[i].pop())
    f.close()
    return dataread,tags

##——————————读取训练好的权重矩阵——————————————————
def readWeights(WeightsPaths):
    f=open(WeightsPaths,"r")
    temp=f.readlines()
    dataread=[]
    tags=[]
    for i in temp:
        dataread.append([float(k) for k in ((i.strip()).split())])
    f.close()
    return dataread

if __name__ == "__main__":
    a=readWeights("syn1.txt")
    print(len(a))
