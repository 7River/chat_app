import socket
import sys
from threading import Thread


list_clients=[]

class Client():
    """docstring for client."""
    def __init__(self,name, addr,connection):
        self.name=name
        self.ip=addr[0]
        self.port=addr[1]
        self.connection=connection

    def data(self):
        return "user:"+self.name+" with ip> "+self.ip+":"+str(self.port)


class ListenThread(Thread):
    """docstring for ListenThread."""
    def __init__(self,client):
        Thread.__init__(self)
        self.client =client

    def run(self):
        while True:
            msg=self.client.connection.recv(1024)
            print(self.client.ip,":",self.client.port,"sent a msg")
            self.send_msg_too_all(msg.decode("utf-8"))

    def send_msg_too_all(self,msg):
        global list_clients
        for i in list_clients:
            if(i==self.client):
                pass
            else:
                i.connection.send(str.encode(self.client.name+">"+str(msg)))




# Create socket (allows two computers to connect)
def socket_create(arg_host,arg_port):
    try:
        global host
        global port
        global s
        host = arg_host
        port = arg_port
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))

    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client (socket must be listening for them)
def socket_accept():
    while True:
        s.listen(5)
        conn, address = s.accept()
        name=conn.recv(1024).decode("utf-8")
        client=Client(name,address,conn)
        list_clients.append(client)
        ListenThread(client).start()
        print("Connection has been established | "+client.data())



def main():
    socket_create('127.0.0.1',9999)
    socket_bind()
    socket_accept()


main()
