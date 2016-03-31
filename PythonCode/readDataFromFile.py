#-*- coding: UTF-8 -*-
#________________________________读取文件数据____________________________________
#______________________________读取标准输入文件__________________________________

def openFilegetData(FilePath):
    f = open(FilePath,'r')
    ff = f.readlines()

    ss=[]
    for s in ff:
        ss.append(s[0:-2].split(" ",3))

    sss=[]
    for i in range(100):
        for s_ in ss[i]:
            sss.append(int(s_))

    data=[]
    FrameCount=13
    pointInput=FrameCount*3+1
    for i in range(7):
        data.append(sss[(pointInput*i):(pointInput*(i+1)-1)])
        data[i].append(-1)#将每组数据最后加上-1元素（阈值）
    #print("data:\n",data)
    return data

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
    data = openFilegetData("Circle.txt")
    [c,d] = readWeights(["weightsyn0.txt","weightsyn1.txt"])
