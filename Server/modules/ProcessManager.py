import warnings

warnings.filterwarnings(action="ignore")
from threading import Thread
from modules.ChildProcess import ChildProcess
import multiprocessing as mp

from modules.Evaluation import GPUusge
from collections import defaultdict
import time


class ProcessManagerThread(Thread):
    def __init__(self, queue, adamm, index):
        super().__init__()
        q = mp.Queue()
        self.index = index

        # TODO: Compare result (Adamm & NON-Adamm)
        # self.adamm = True : Run Adamm -
        # self.adamm = False : baseline
        self.adamm = True  # True --> adamm False -> one-server
        self.image_queue_process = q
        self.start_flag = 0
        self.gpu = GPUusge(defaultdict(list))
        self.image_queue = queue
        self.current_process = None  # 현재 만들어져있는 프로세스. None->프로세스 없음
        # TODO : Change using LSTM result (self.timeout)
        self.timeout = 1
        self.waiting_time = 0
        self.waiting_flag = 0
        self.image_queue_process_size = 40
        self.queue_drop = 0
        self.filename = "../data/test_one"

        if self.adamm:
            self.filename = "../data/test.log"

    def run(self):
        start_time = 0
        # TODO: DataManager 쓰레드로부터 데이터 받기
        # TODO: 프로세스 불러오거나 생성
        # TODO: 만들어진 (혹은 가져온) 프로세스에게 데이터 전달
        while True:
            try:
                image = self.image_queue.get(timeout=1)
                print("[System] image process size {0}".format(self.image_queue_process.qsize()))
                if type(image) is str:
                    print(" [System]{0} Image End socket".format(self.index))
                    while True:
                        if self.image_queue_process.qsize() == 0:
                            print("[System] {0} End Process Manger".format(self.index))
                            self.start_flag = 2
                            if self.current_process is not None:
                                self.terminate_process()
                            break

                if self.start_flag == 2:
                    print("End")
                    print("End time", time.time() - start_time)
                    # time.sleep(1)
                    self.gpu.write_file(self.file_name)
                    print("frame drop", self.queue_drop)
                    print("writing")
                    self.gpu.stop()
                    self.gpu.join()
                    break

                if self.current_process is None:
                    if self.start_flag == 0:
                        self.gpu.start()
                        print("gpu start")
                        start_time = time.time()
                        print("start_time")
                        self.start_flag = 1
                    self.create_process()
                    print("Create", self.index, self.current_process, id(self.current_process))

                self.execute_process(image)

            except Exception:
                print("[System] image process size {0}".format(self.image_queue_process.qsize()))
                print("[System] {0} Timeout".format(self.index))
                # print("[System] image process size {0}".format(self.image_queue_process.qsize()))
                if self.start_flag == 2:
                    if self.current_process is not None:
                        self.terminate_process()
                    # print("End")
                    # print("End time", time.time() - start_time)
                    # time.sleep(1)
                    self.gpu.write_file(self.file_name)
                    # print("frame drop", self.queue_drop)
                    # print("writing")
                    self.gpu.stop()
                    self.gpu.join()
                    break

                if self.image_queue_process.qsize() == 0 and self.current_process is not None:
                    print("[System] IN")
                    if self.waiting_flag == 0:
                        self.waiting_time = time.time()
                        self.waiting_flag = 1
                        # print("[System] start waiting", self.waiting_time)
                    else:
                        print("[System] waiting time",time.time()-self.waiting_time)
                        if time.time() - self.waiting_time > self.timeout:
                            print("[System] {0} Timeout processing queue".format(self.index))
                            self.waiting_flag = 0
                            if self.current_process is not None:
                                print("[System] {0} Process stop".format(self.index))
                                self.terminate_process()
                                print("[System] Process Manager", self.index, self.current_process,
                                      id(self.current_process))

    def execute_process(self, image):
        try:
            self.image_queue_process.put(image, block=False)
            self.waiting_flag = 0
            # self.current_process.run()
        except Exception:
            self.queue_drop += 1
            pass

    def create_process(self):
        q = mp.Queue(maxsize=self.image_queue_process_size)
        self.image_queue_process = q
        self.current_process = ChildProcess(q)
        self.current_process.start()

    def terminate_process(self):
        if self.adamm:
            self.current_process.terminate()
            self.current_process.join()  # stop 기다리기
            # print("[System] terminate!!!")
            self.current_process = None
        else:
            pass
