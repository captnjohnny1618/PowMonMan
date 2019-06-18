import sys
import os
import datetime

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
