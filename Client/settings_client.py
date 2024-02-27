import os
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]          # settings directory (root)
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

WEIGHT_PATH = ROOT / 'config/weights/yolov7-tiny.pt'  # path to the weight file
HOST_IP = '127.0.1.1' #'192.9.202.212' #'192.168.56.1' #192.9.202.212     # paste your server ip address here
PORT1 = 9999                # port for first detection instance
PORT2 = 12345               # port for second detection instance

VIEW_TRANSMITTING = False   # view transmitting video file window
CLASSES_LIST = list(range(80))  # list of the clsses to detect

FRAME_WIDTH = 720          # window width of the detection

CLIENT_TIMEOUT = 60         # time out of the client for one instance of the client

VIDEO_FILENAME = 'test.mp4'
VIDEO_PATH = ROOT / f'config/datainput/videos'
VIDEO_DIRPATH = ROOT / 'videos'
