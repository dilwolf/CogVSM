import socket
import time
import numpy as np
import cv2
client_socket = socket.socket()

ip_address="127.0.0.1" #Edge node Ip address
client_socket.connect((ip_address, 8000))  # ADD IP HERE

connection = client_socket.makefile('wb')
i=0
video_path="../video/v3.mp4"
cam = cv2.VideoCapture(video_path)

while True:
    start_time=time.time()
    ret, img = cam.read()
    if ret is None:
        break
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()
    time.sleep(0.5)

    if i==10:
        #client_socket.send(str(len(a)).ljust(16).encode())
        time.sleep(20)
    else:
        print("Send {}".format(i))
        client_socket.send(str(len(stringData)).ljust(16).encode())
        client_socket.send(stringData)

    i+=1
