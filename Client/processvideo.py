import threading
import time
import cv2
import ffmpeg
#import yolov5
import yolov7
import settings_client
import os


def load_ml_model():
    print("[INITIATE] model loading...")

    # load pretrained model
    model = yolov7.load(settings_client.WEIGHT_PATH)

    # set model parameters
    model.conf = 0.25
    model.iou = 0.45
    model.agnostic = False
    model.classes = settings_client.CLASSES_LIST
    print("[SUCCESS] model loading done.")
    return model


class VideoLoader:
    def __init__(self):
        print("[Video Loader Active...]")

    def load_local_vid(self, filename):
        print("Load local video active...")
        vid = cv2.VideoCapture(os.path.join(
            settings_client.VIDEO_PATH, filename))
        vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        print("vid is:", vid)
        return vid

    def load_stream(self, streampath):
        print("Load stream active...")
        vid = cv2.VideoCapture(os.path.join(
            settings_client.VIDEO_PATH, streampath))
        vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        print("vid is:", vid)
        return vid

    def load_webcam(self):
        print("Load webcam active...")
        vid = cv2.VideoCapture(0)
        vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        return vid


class MLModule:
    def __init__(self, ):
        pass


if __name__ == '__main__':
    thread_camera = VideoLoader(0)
    while True:
        try:
            thread_camera.show_frame()
        except:
            pass
