##____________________包含串口读取以及数据解析两个方法________________________
##
##注注注注：数据的帧设计可以不用“-”负号，使用多一位作为标志位，这样更容易处理，降低处理时间和性能消耗

import serial

SingleGroupData =[[0]*40]
readCom_StopFlag = False #TODO：此为串口读写线程退出的条件；添加：等待后续整理完决定
FrameperGroup=13
def readCom(ComNumber="COM3"):
    print(threading.currentThread().getName()+' On')#打印当前线程名
    com=None
    try:
        com=serial.Serial(ComNumber,9600)
        print(com.portstr)
        global SingleGroupData,readCom_StopFlag, FrameperGroup
        while True:
            ##以下两个为全局变量，储存串口读取的字符串和解析后的数据
            ##帧数同步
            print(threading.currentThread().getName()+' On')#打印当前线程名
            try:
                lock.acquire()
                while True:
                    print("Tag the while")
                    ch = com.read(1)
                    if ch == b'h':
                        print("Tag break")
                        break
                SingleGroupStr=com.read(10*FrameperGroup-1)#每帧数据由10个字符组成共13帧，预留一帧同步
                SingleGroupData=translateStr(SingleGroupStr)
                if SingleGroupData !=[[0]*40]:
                    print(SingleGroupData)
            finally:
                lock.release()
            ##TODO:以下为关闭串口读写的条件
            if readCom_StopFlag:
                break
    finally:
        if com != None:
            com.close()

def chr3_2int(str_):
    int_=0
    sign=1
    for i in range(3):
        if str_[i]=='-':
            sign=-1
        else:
            int_=10*int_+int(str_[i])
    int_ = sign*int_
    return int_

#只能慢慢切片：
def translateStr(Str):
    global FrameperGroup
    Strs=str(Str,"utf-8")
    #每帧等分三分
    Temp=[]
    for i in range(FrameperGroup):
        for j in range(3):
            Temp.append(chr3_2int(Strs[j*3+i*10:j*3+3+i*10]))
    Temp.append(-1)
    return Temp

def judgeConnectedCOMNum():
    pass

if __name__ == "__main__":
    readCom("COM3")