import threading
from threading import Thread
import re
import ipywidgets as widgets
from subprocess import check_output
import csv
import time
import os
from subprocess import Popen, PIPE
import logging


class GPUusge(Thread):
    def get_log(self):
        logger_file = logging.getLogger("File")
        logger_file.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("../data/" + "test.log", mode="w")
        formatter = logging.Formatter(' %(name)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger_file.addHandler(stream_handler)
        logger_file.addHandler(file_handler)

        return logger_file

    def __init__(self, usage_dict):
        super().__init__()
        self.usage_list = usage_dict
        self.stop_flag = threading.Event()
        self.file_logger = self.get_log()

    def stop(self):
        self.stop_flag.set()

    def stopped(self):
        return self.stop_flag.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            self.getGPU()
            time.sleep(0.5)

    def getlist(self):
        return self.usage_list

    def safeFloatCast(self, strNumber):
        try:
            number = float(strNumber)
        except ValueError:
            number = float('nan')
        return number

    def getGPU(self):
        p = Popen(['nvidia-smi',
                   "--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu",
                   "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderror = p.communicate()
        output = stdout.decode('UTF-8')
        lines = output.split(os.linesep)
        vals = lines[0].split(",")
        self.match_list(vals)

    def write_file(self, filename):
        result = self.getlist()
        config = filename + ".csv"
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for k, v in result.items():
                writer.writerow([k] + v)
        print("[System] End of writing file", len(self.usage_list["GPU"]))
   

    def match_list(self, vals):
        for i in range(12):
            # print(vals[i])
            if (i == 0):
                deviceIds = (vals[i])
            elif (i == 1):
                uuid = vals[i]
            elif (i == 2):
                gpuUtil = self.safeFloatCast(vals[i]) / 100
            elif (i == 3):
                memTotal = self.safeFloatCast(vals[i])
            elif (i == 4):
                memUsed = self.safeFloatCast(vals[i])
            elif (i == 5):
                memFree = self.safeFloatCast(vals[i])
            elif (i == 6):
                driver = vals[i]
            elif (i == 7):
                gpu_name = vals[i]
            elif (i == 8):
                serial = vals[i]
            elif (i == 9):
                display_active = vals[i]
            elif (i == 10):
                display_mode = vals[i]
            elif (i == 11):
                temp_gpu = self.safeFloatCast(vals[i])

        self.usage_list["GPU"].append(gpuUtil * 100)
        self.usage_list["Memory"].append(float(memUsed) / float(memTotal) * 100)

        self.file_logger.debug("{0};{1}".format(gpuUtil * 100, float(memUsed) / float(memTotal) * 100))

        print("GPU", gpuUtil * 100, "Usage_list", len(self.usage_list["GPU"]))
        print("Memory", float(memUsed) / float(memTotal) * 100)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
