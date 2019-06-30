import sys
import os
import _thread
from .udp import udp_broadcaster
from .filehandling import makeDirIfDoesntExist, makeFileIfDoesntExist, writePermissionsCheck, deleteFileIfExists
from .configure import loadConfigurationFile
import datetime
import socket
import daemon
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import shutil

class PowMonManServer:
    platform           = sys.platform
    port_number        = 7444
    udp_port_number    = port_number-1
    power_check_module = "RPi"
    power_check_pin    = 4
    power_check_file   = "/var/local/PowMonMan/ON"
    logdir_path        = "/var/log/PowMonMan/"

    def __init__(self,config):
        self.port_number        = config['ServerClient']['port_number']
        self.udp_port_number    = config['ServerClient']['udp_port_number']
        self.power_check_module = config['PowerCheck']['module']
        self.power_check_file   = config['Platform'][self.platform]['power_check_file']
        self.power_check_pin    = config['Modules']['RPi']['status']
        self.logdir_path        = config['Platform'][self.platform]['log_dir']
        self.logfile_path       = os.path.join(self.logdir_path,'server.log')
        
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
        with conn:
            pin_status = os.path.isfile(self.power_check_file)            
            if pin_status:
                conn.sendall(bytes("on",'utf-8'))
            else:
                conn.sendall(bytes("off",'utf-8'))

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
        makeDirIfDoesntExist(self.logdir_path)
        makeFileIfDoesntExist(self.logfile_path)
        writePermissionsCheck(self.logfile_path)

        self.logger = logging.getLogger('server')
        #hdlr = logging.FileHandler(self.logfile_path)
        hdlr = TimedRotatingFileHandler(self.logfile_path,when='midnight',interval=1,backupCount=7)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        hdlr.suffix = "%Y%m%d"
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

def main():

    with daemon.DaemonContext(stdout=sys.stdout,stderr = sys.stderr):
        config = loadConfigurationFile()
        P = PowMonManServer(config)
        P.startLogging()
        P.run()
    
if __name__=="__main__":
    main()
