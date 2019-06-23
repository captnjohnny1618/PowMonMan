import sys
import os
import _thread
from .udp import udp_broadcaster
from .filehandling import makeDirIfDoesntExist, makeFileIfDoesntExist, writePermissionsCheck, deleteFileIfExists
import socket
import daemon
import time
import logging

class PowMonManServer:
    port_number = 7444
    udp_port_number = port_number-1
    power_check_module  = "RPi"
    power_check_pin = 4
    power_check_file = "/var/local/PowMonMan/ON"
    
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
        self.logger.info("Starting UDP broadcasts...")        
        while True:
            with udp_broadcaster(self.udp_port_number,"PowMonMan Server!"):
                pass
            if not is_broadcasting:
                is_broadcasting = True
                self.logger.info("UDP broadcasts running")
            time.sleep(5)

    def clientThread(self,conn):

        pin_status = os.path.isfile(filepath);
        
        if pin_status:
            conn.sendall(bytes("on",'utf-8'))
        else:
            conn.sendall(bytes("off",'utf-8'))
        conn.close()

    def powerCheckThread(self):
        is_running = False
        self.logger.info("Starting power check thread...")
        if self.power_check_module == "RPi":
            import RPi.GPIO as gpio
            gpio.setmode(gpio.BCM)
            gpio.setup(self.power_check_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
            while True:
                power_is_on = gpio.input(self.power_check_pin)
                if power_is_on:
                    makeDirIfDoesntExist(os.path.dirname(self.power_check_file))
                    makeFileIfDoesntExist(self.power_check_file)
                else:                    
                    deleteFileIfExists(self.power_check_file)

                if not is_running:
                    is_running = True
                    self.logger.info("Power check thread running")
                    
                time.sleep(1)

    def run(self):
        _thread.start_new_thread(self.powerCheckThread,())
        time.sleep(1)
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
