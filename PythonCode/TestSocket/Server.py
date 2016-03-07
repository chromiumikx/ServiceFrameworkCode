import socket   #socket模块
import commctrl  #执行系统命令模块
HOST='127.0.0.1'
PORT=50036
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
s.bind((HOST,PORT))   #套接字绑定的IP与端口
s.listen(5)         #开始TCP监听
print("socket listening")
while 1:
    conn,addr=s.accept()   #接受TCP连接，并返回新的套接字与IP地址
    print('Connected by',addr)    #输出客户端的IP地址
    while 1:
        data=conn.recv(1024).decode()    #把接收的数据实例化
        if data=="cmd":
            print("Done.")
            conn.sendall(('Done.').encode())
conn.close()     #关闭连接
