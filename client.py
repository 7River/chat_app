import os
import socket
import subprocess
from threading import Thread
from cryptography.fernet import Fernet



key = b'eAQRejSYaDhPmGD9-HJ_6-hyG_R7mqE40KH4sxOUtIg='
encryption_decryption_suite =Fernet(key)


class ListenThread(Thread):
    """docstring for ListenThread."""
    def __init__(self,sock):
        Thread.__init__(self)
        self.socket =sock

    def run(self):
        while True:
            msg=self.socket.recv(1024).decode('utf-8').split('>')
            dec_msg=encryption_decryption_suite.decrypt(msg[1].encode('utf-8'))
            print(msg[0],'>',dec_msg.decode('utf-8'))


# Create a socket
def socket_create(arg_host,arg_port):
    try:
        global host
        global port
        global s
        host = arg_host
        port = arg_port
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " ,msg)


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        global name
        s.connect((host, port))
        ListenThread(s).start()
        # s.send(name)
    except socket.error as msg:
        print("Socket connection error: " ,msg)



def main():
    global name
    global s
    name=input("your name:")

    socket_create('127.0.0.1',9999)
    print("socket created")
    socket_connect()
    print("socket connected")
    s.send(str.encode(name))

    while True:
        msg=input()
        print("me>",msg)
        enc_msg=encryption_decryption_suite.encrypt(str.encode(msg))
        s.send(enc_msg)



name=""
main()
