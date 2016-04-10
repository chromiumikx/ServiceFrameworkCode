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
    s=[]
    for path in WeightsPaths:
        f=open(path,'r')
        ff=f.readlines()
        ss=[]
        for line in ff:
            sss=line.split(" ")
            sss.pop(len(sss)-1)
            for i in range(len(sss)):
                sss[i]=float(sss[i])
            ss.append(sss)
        s.append(ss)
    return (s)

if __name__ == "__main__":
    data,tags = openFilegetData()
    [c,d] = readWeights(["weightsyn0.txt","weightsyn1.txt"])
