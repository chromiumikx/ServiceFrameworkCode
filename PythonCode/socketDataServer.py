#coding:utf-8

import sys
import socket
import json as js


#TODO:此处两个标记全局变量标记server与client连接开启情况；添加：待后续测试决定；
BreakCondition = False
Condition = False
def socketDataServer(input_HOST='127.0.0.1', input_PORT=50033, input_backlog = 1):
    print(threading.currentThread().getName()+' On')#打印当前线程名
    global GestureNum, BreakCondition, Condition
    ##以下为 为API提供全局资源，供用户读取
    global OneFrame
    HOST=input_HOST
    PORT=input_PORT
    backlog = input_backlog
    
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print ("Failed to create socket")
        sys.exit()
    print ("Server_Socket Created")
    
    try:
        s.bind((HOST,PORT))
    except socket.error as msg:
        s.close()
        print ('Bind failed. Error Code:'+str(msg[0])+' Message '+str(msg[1]))
        sys.exit()
    print ("Socket bind complete")
    
    s.listen(backlog)
    print ("Socket is now listening")
    
    while True:
        conn,addr=s.accept()
        print ("Connected with "+addr[0]+':'+str(addr[1]))
        try:
            ##以下为指令处理模块，连接SDK中的API
            while True:
                RequireComm=conn.recv(1024).decode()
                if RequireComm == "Gesture":
                    print("Get cmd of Gesture")
                    conn.sendall((str(GestureNum)).encode())
                    GestureNum=0
                elif RequireComm == "Accs":
                    Accs=OneFrame[0:3]
                    ##还要将此list转成json或其他格式
                    conn.sendall(js.dumps(Accs))
                    OneFrame=[[0]*6]
                elif RequireComm == "Rots":
                    Rots=OneFrame[0:3]
                    ##还要将此list转成json或其他格式
                    conn.sendall(js.dumps(Rots))
                    OneFrame=[[0]*6]
                else:
                    #以下一句只是指接收到的命令不是“Gesture”时所做的处理，并非是说没接到指令
                    conn.sendall((" ").encode())

                print(threading.currentThread().getName()+' On')#打印当前线程名

                time.sleep(0.05)#为让线程不占用全部cpu

                if BreakCondition:
                    break        
            if Condition:
                break
        except:
            conn.close()
            pass

    s.close()

if __name__ == "__main__":
    socketDataServer()
