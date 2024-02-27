from threading import Thread
import cv2
import struct
import pickle
import numpy as np
import time
import onnxruntime as rt

sess = rt.InferenceSession('tf-pose-estimation/lstm_model/model1.onnx', device="cpu")
input_name = sess.get_inputs()[0].name

WINDOW_SIZE, alpha, theta = 5, 0.9, 3
arr_of_num = [1,1,1,1,1]

def make_prediction(m):
    global arr_of_num
    arr_of_num.append(m)
    if len(arr_of_num)>WINDOW_SIZE:
        arr_of_num = arr_of_num[1:]
    if len(arr_of_num)==WINDOW_SIZE:
        actual = arr_of_num[-1]
        input_data = np.array(arr_of_num[-WINDOW_SIZE:], dtype=np.float32).reshape(1, WINDOW_SIZE, 1)
        forecast = sess.run(None, {"input": input_data})[0][0][0]

        return forecast #actual

class DataManagerThread(Thread):
    def __init__(self, queue,sock, index):  
        super().__init__()
        
        self.image_queue = queue
        self.server_socket = sock  
        self.index = index
        
        
    def run(self):
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = self.server_socket.recv(4*1024)
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += self.server_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            data_dict = pickle.loads(frame_data)
            # extract frame and detection information from data dictionary
            img = data_dict['frame']
            people = data_dict['people'] 
            pred = make_prediction(people)
            print(f"Detected:{people}, Predictions:{pred}")
            self.put_data_to_queue(img) if people != 0 else None
            # if pred != 0:
            #     self.put_data_to_queue(img)

    def put_data_to_queue(self, image):
        self.image_queue.put(image)