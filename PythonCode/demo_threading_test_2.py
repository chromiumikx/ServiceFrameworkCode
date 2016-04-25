#############    使用GR_SDK一个Gemo    #################
#使用方法：1.调用SDK中的Connect类建立一个连接
#2.调用get***()函数得到相应数据

import time,threading
import GR_SDK

#Demo
def creatmyclient():
    myclient =GR_SDK.ClientConnect()#1.建立连接
    Dict = {1:"圆",2:"三角形",3:"<<<左滑动",4:"右滑动>>>"}
    t0=time.clock()
    Num = ""
    while Num != "No_Connect":
        Num = myclient.getGesture()#2.请求（规定）数据
        if Num != "0":
            print("当前的动作是：——",Dict[Num])
        time.sleep(0.05)

        if time.clock() - t0 > 60:
            break
    print(Num)
    
    myclient.stop()

tClient=threading.Thread(target=creatmyclient)
time.sleep(1)
tClient.start()
tClient.join()
