import sys
import os
import _thread
from .udp import udp_broadcaster
from .filehandling import makeDirIfDoesntExist, makeFileIfDoesntExist, writePermissionsCheck
import socket
import daemon
import time
import logging

class PowMonManServer:
    port_number = 7444
    udp_port_number = port_number-1

    def handleRequests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', self.port_number))
            except socket.error as msg:
                self.logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                sys.exit()

            s.listen(10)
            
            while True:                
                conn, addr = s.accept() # blocking call (waits for connection)
                self.logger.info('Connected with ' + addr[0] + ':' + str(addr[1]))
                _thread.start_new_thread(self.clientThread,(conn,))
                
            s.close()
    
    def udpBroadcastThread(self):
        is_broadcasting = False
        print("Starting UDP broadcast...")
        while True:
            with udp_broadcaster(self.udp_port_number,"PowMonMan Server!"):
                pass
            if not is_broadcasting:
                is_broadcasting = True
                print("UDP broadcasts: running")
            time.sleep(5)

    def clientThread(self,conn):

        filepath = "/var/local/PowMonMan/ON"
        pin_status = os.path.isfile(filepath);
        
        if pin_status:
            conn.sendall(bytes("on",'utf-8'))
        else:
            conn.sendall(bytes("off",'utf-8'))
        conn.close()        
                
    def run(self):
        _thread.start_new_thread(self.udpBroadcastThread,())
        self.handleRequests()


    def startLogging(self):
        logdir_path = '/var/log/PowMonMan/'
        logfile_path = '/var/log/PowMonMan/server.log'

        makeDirIfDoesntExist(logdir_path)
        makeFileIfDoesntExist(logfile_path)
        writePermissionsCheck(logfile_path)

        self.logger = logging.getLogger('server')
        hdlr = logging.FileHandler(logfile_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

def main():
    with daemon.DaemonContext(stdout=sys.stdout,stderr = sys.stderr):
        P = PowMonManServer()
        P.startLogging()
        P.run()
    
if __name__=="__main__":    
    main()
