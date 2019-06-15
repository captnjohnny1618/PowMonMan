import sys
import daemon
import time

import datetime
import socket

class shutdown_timer:
    is_timing = False
    start_time = datetime.datetime.now()
    
    def start(self):
        self.is_timing = True
        self.start_time = datetime.datetime.now()
        
    def stop(self):
        self.is_timing = False

    def get_elapsed(self):
        if self.is_timing:
            elapsed = (datetime.datetime.now() - self.start_time).total_seconds()
        else:
            elapsed = -1            
        return elapsed
    
def check_power_server():
    # Open socket    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        print("Failed to create socket")
        sys.exit()

    host = "localhost" # debugging
    port = 7444

    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
        
    #print('Ip address of ' + host + ' is ' + remote_ip)

    s.connect((remote_ip,port))
    data = s.recv(4096);
    return data.decode("utf-8")
    
def do_something():
    shutdown_time = 30;
    t = shutdown_timer();
    prev_power_state = True
    power_state = True

    while True:
        
        power_state = check_power_server()

        # Power has switched
        if power_state != prev_power_state:        
            if power_state == "true":
                increment = 5;
                t.stop()
            elif power_state == "false":
                t.start()
                increment = 1;
            else:
                print("ERROR received incorrectly formatted data from power server")
                increment = 5;

        else:
            if power_state == "false":
                elapsed = t.get_elapsed()
                if  elapsed > shutdown_time:
                    cmd = "sudo shutdown -h now"
                    print(cmd)
                else:
                    print("{} seconds until shutdown!".format(shutdown_time-elapsed))

        prev_power_state = power_state;
        time.sleep(increment)

def run():
    with daemon.DaemonContext(stdout = sys.stdout,stderr = sys.stderr):
        do_something()

if __name__ == "__main__":
    run()
