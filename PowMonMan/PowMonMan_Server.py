import sys
import os
import _thread
from udp import udp_broadcaster
import socket
import daemon
import time

class PowMonManServer:
    port_number = 7444
    udp_port_number = port_number-1

    def handleRequests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', self.port_number))
            except socket.error as msg:
                print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                sys.exit()

            s.listen(10)
            
            while True:                
                conn, addr = s.accept() # blocking call (waits for connection)
                print('Connected with ' + addr[0] + ':' + str(addr[1]))
                _thread.start_new_thread(self.clientThread,(conn,))
                
            s.close()
    
    def udpBroadcastThread(self):
        while True:
            with udp_broadcaster(self.udp_port_number,"PowMonMan Server!"):
                pass
            time.sleep(5)

    def clientThread(self,conn):
        pin_status = os.path.isfile("/Users/johnhoffman/Code/PowMonMan/ON");
        
        if pin_status:
            conn.sendall(bytes("on",'utf-8'))
        else:
            conn.sendall(bytes("off",'utf-8'))
        conn.close()        
                
    def run(self):
        _thread.start_new_thread(self.udpBroadcastThread,())
        self.handleRequests()


def main():
    with daemon.DaemonContext(stdout=sys.stdout,stderr = sys.stderr):
        P = PowMonManServer()
        P.run()
    
if __name__=="__main__":    
    main()
