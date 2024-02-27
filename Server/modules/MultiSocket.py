import threading
from modules.DataManager import DataManagerThread
from modules.ProcessManager import ProcessManagerThread
from queue import Queue


class MultiSocket(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def run(self):
        global index
        conn, addr = self.s.accept()
        print("[System] Connect client {0}".format(index))
        # data manager & process manager 실행
        image_queue = Queue()

        dataManager = DataManagerThread(image_queue, conn, index)

        processManager = ProcessManagerThread(image_queue, True, index)

        dataManager.start()
        processManager.start()

        index += 1
        create_thread(self.s)


thread_list = []
index = 0


def create_thread(sock):
    global index
    thread_list.append(MultiSocket(sock))
    thread_list[index].start()
