import socket
import cv2
import pickle
import imutils
import time
import struct
import sys
from collections import Counter
from ast import literal_eval
import settings_client
import processvideo

model = processvideo.load_ml_model()  # Load machine learning model

class ThreadedClient(object):
    def __init__(self, host, port, number, vidname=None, stream=None):
        self.vidname = vidname
        self.stream = stream
        self.host = host
        self.port = port
        self.number = number

        self.fps = 1/60
        self.fps_ms = int(self.fps*1000)

        self.prepare_socket()

    def prepare_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[SUCCESS] Socket created.")

    def connect(self):
        try:
            self.address = (self.host, self.port)
            self.sock.connect(self.address)
            print("[SUCCESS] Connected to server at: ", self.address)
        except socket.error as msg:
            print('Connect failed. Error : ' + str(sys.exc_info()))
            sys.exit()

    def send_data(self):
        vidfl = processvideo.VideoLoader()
        if self.vidname:
            vid = vidfl.load_local_vid(self.vidname)
        elif self.stream:
            vid = vidfl.load_stream(self.stream)
        else:
            vid = vidfl.load_webcam()
        data_dict = {}
        while (vid.isOpened()):
            img, frame = vid.read()
            #print(self.fps)
            #time.sleep(self.fps)

            
            results = model(frame)
            #labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

            results_list = results.pandas().xyxy[0].to_json(orient="records")
            results_list = literal_eval(results_list)
            classes_list = [item["name"] for item in results_list]
            people = classes_list.count('person')
            #results_counter = Counter(classes_list)
            #print(results_counter)
            results.render()

            frame = imutils.resize(
                frame, width=settings_client.FRAME_WIDTH)
            data_dict['frame'] = frame
            data_dict['people'] = people
            a = pickle.dumps(data_dict)
            message = struct.pack("Q", len(a))+a
            time.sleep(1/25)
            try:
                # send message or data frames to client
                self.sock.sendall(message)
            except Exception as e:
                print(e)
                raise Exception(e)
            if settings_client.VIEW_TRANSMITTING:
                cv2.imshow(
                    f'TRANSMITTING VIDEO {self.number}', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
        self.sock.close()

def main():
    host_ip = '192.9.202.212' # Here according to your server ip write the address
    port =  9998   #port = int(input())
    print('HOST IP:', host_ip)
    while True:
        port_num = port
        try:
            port_num = int(port_num)
            break
        except ValueError as e:
            print(e)
            pass

    client = ThreadedClient(host_ip, port_num, 1, 'test.mp4')
    client.connect()
    client.send_data()

if __name__ == "__main__":
    main()
