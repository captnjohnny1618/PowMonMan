import sys
import os
import socket

# Broadcast on 7443
# TCP on 7444

class udp_receiver:
    def __init__(self, port, msg_leng=8192, timeout=15):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.settimeout(timeout)
        self.sock.bind(('',port))
        self.msg_leng = msg_leng

    def __iter__(self):
        return self

    def __next__(self):
        try:
            addr,data = self.sock.recvfrom(self.msg_leng)
            data = data.decode('utf-8')
            return addr, data
        except Exception as e:
            print("Exception encountered while executing UDP recv: {}".format(e))
            raise StopIteration
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

class udp_broadcaster:
    def __init__(self,port,data_string):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        self.sock.sendto(bytes(data_string.encode('utf-8')),('255.255.255.255',port))
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
