#coding=utf-8
import socket
import sys
import json as js

#warning TODO:编写SDK/API文档

class ClientConnect:
    def __init__(self, host='127.0.0.1', port=50033):
        self.HOST = host
        self.PORT = port
        self.client_socket=None
        self.isConnect=False
        self.start_connect()
        

    def __def__(self):
        print("Exiting the client")
        self.client_socket.close()

    def stop(self):
        self.client_socket.close()

    def start_connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print ("Socket Creating")
        except socket.error:
            print("Failed to create socket")
            #sys.exit()
        
        try:
            self.isConnect=True
            print ("Connecting",self.isConnect)
            self.client_socket.connect((self.HOST, self.PORT))
        except socket.error:
            self.isConnect=False
            print ("Failed to connect the server",self.isConnect)
            #sys.exit()

    def getGesture(self):
        #若连接建立不成功，直接返回没有连接的提醒代码
        if not self.isConnect:
            return "No_Connect"
        flag=True
        receive_data=""
        while (receive_data==" ") or (receive_data==""):
            self.client_socket.sendall(("Gesture").encode())
            receive_data = self.client_socket.recv(1024).decode()
            #print("receive_data:",receive_data)

        return receive_data

    #TODO:向外提供传感器加速度的原始数据；实现：等主要部分完成再加上，需要确定发送的命令，服务器上接受的命令和发送的数据要做添加
    def getAccs(self):
        #若连接建立不成功，直接返回没有连接的提醒代码
        if not self.isConnect:
            return "No_Connect"
        flag=True
        receive_data=[]
        while (receive_data==" ") or (receive_data==""):
            self.client_socket.sendall(("Accs").encode())
            receive_data = js.loads(self.client_socket.recv(1024))
            #print("receive_data:",receive_data)

        return receive_data

    def getRots(self):
        #若连接建立不成功，直接返回没有连接的提醒代码
        if not self.isConnect:
            return "No_Connect"
        flag=True
        receive_data=[]
        while (receive_data==" ") or (receive_data==[]):
            self.client_socket.sendall(("Rots").encode())
            receive_data = js.loads(self.client_socket.recv(1024))
            #print("receive_data:",receive_data)

        return receive_data
