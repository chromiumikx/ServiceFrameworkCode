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
def readWeights(WeightsPath1, WeightsPath2):
    f=open(WeightsPath1,'r')
    ff=f.readlines()
    
    ss=[]
    for line in ff:
        ss.append(float(line[:-1]))
    
    f=open(WeightsPath2,'r')
    ff=f.readlines()
    
    ss1=[]
    for line in ff:
        sss=line.split(" ",39)
        for i in range(40):
            sss[i]=float(sss[i])
        
        ss1.append(sss)
    
    return (ss, ss1)

if __name__ == "__main__":
    data = openFilegetData("Circle.txt")
    #readWeights("weightsyn1.txt")
    d1, d0 = readWeights("weightsyn1.txt","weightsyn0.txt")