import sys
import os
import time
import daemon

import socket
from timer import shutdown_timer
from udp import udp_receiver

class PowMonManClient:

    port_number = 7444
    udp_port_number = port_number-1
    server_ip = [];
    timer = shutdown_timer()
    shutdown_time = 10 #600 
    poll_rate = 5
    
    def __init__(self):
        print("Starting PowMonMan_Client...")              
        self.server_ip = self.listenForServer()              
        if not self.server_ip:
            print("Could not find a server on the network!")
        else:
            print("    Server found at:      {}\n".format(self.server_ip) + 
                  "    Using port:           {}\n".format(self.port_number) + 
                  "    Shutdown time (sec):  {}\n".format(self.shutdown_time) + 
                  "    Current power status: {}".format(self.checkPowerState()))
              
    def listenForServer(self):
        # Add UDP discovery code
        print("Listening for PowMonMan server...",end="",flush=True)
        packets_received = 0
        with udp_receiver(udp_port_number) as ur:
            for (address,data) in ur:
                print(".",end="",flush=True)
                if data == "PowMonMan Server!":
                    print("Found! ({})".format(address))
                    return address
                else:
                    continue
                    
                packets_received+=1
                
                if packets_received>10:
                    print("")
                    print("Receiving packets, however they're not what I expect...\n" + 
                          "Guessing that the server address is {}\n".format(address) +
                          "however this may be incorrect.  Double check server configuration\n" +
                          "if PowMonMan is not functioning correctly.\n")
                    return address
        return []
        #return("192.168.3.106")

    def checkPowerState(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print("Failed to create socket")
            sys.exit()
            
        try:
            s.connect((self.server_ip,self.port_number))
            data = s.recv(4096)
            return(data.decode("utf-8"))
        except:
            print("Unable to connect to server.")
            return("error connecting")

    def sendShutdownSignal(self):
        print("SHUTDOWN INITIATED")
        
        if sys.platform in ["darwin","linux"]:
            cmd = "sudo shutdown -h now"
        if sys.platform in ["win32"]:
            cmd = "shutdown /s"

        from subprocess import call        
        call(cmd.split())
        sys.exit(0);

    def run(self):
        power_state      = "on"
        prev_power_state = "on"

        while True:
            
            power_state = self.checkPowerState()
            
            if (power_state != prev_power_state) and (power_state=="on"):
                self.poll_rate = 5
                self.timer.stop()
            elif (power_state != prev_power_state) and (power_state=="off"):
                self.poll_rate = 1
                self.timer.start()
            elif (power_state == prev_power_state) and (power_state=="off"):
                elapsed = self.timer.get_elapsed()
                if elapsed > self.shutdown_time:
                    self.sendShutdownSignal()
                else:
                    print("{} seconds until shutdown!".format(round(self.shutdown_time - elapsed)))

            prev_power_state = power_state
            time.sleep(self.poll_rate)

if __name__=="__main__":

    with daemon.DaemonContext(stdout = sys.stdout, stderr = sys.stderr):
        P = PowMonManClient();
        P.run()
