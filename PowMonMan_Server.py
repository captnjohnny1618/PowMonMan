import sys
import os
import _thread
from udp import udp_broadcaster
#from threading import Thread

import socket

def client_thread(conn):
    # check pin status
    pin_status = os.path.isfile("ON");
    
    if pin_status:
        conn.sendall(bytes("true",'utf-8'))
    else:
        conn.sendall(bytes("false",'utf-8'))
    conn.close()        

def main():

    HOST = ''    # Symbolic name, meaning all available interfaces
    PORT = 7444    # Arbitrary non-privileged port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Socket created')
     
        #Bind socket to local host and port
        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        
            print('Socket bind complete')
     
            #Start listening on socket
        s.listen(10)
        print('Socket now [el for el in list]stening')
     
        #now keep talking with the client
        while True:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()        
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
            _thread.start_new_thread(client_thread,(conn,))
     
        s.close()

if __name__=="__main__":

    port_number = 7444
    udp_port_number = port_number-1

    while True:
        with udp_broadcaster(udp_port_number,"PowMonMan Server!"):
            print("Broadcasting server identification packet...")

    main();
