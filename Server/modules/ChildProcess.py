import warnings

warnings.filterwarnings(action="ignore")
from multiprocessing import Process
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import argparse
import cv2
import logging
import time


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def init_logger():
    logger = logging.getLogger('TfPoseEstimator-WebCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class ChildProcess(Process):
    def __init__(self, queue):
        self.start_time = time.time()
        super().__init__()
        self.image_queue = queue
        # self.message_queue=msg
        self.start_time = time.time()
        # self.gpu=gpu

    def __del__(self):
        pass

    # Start 혹은 run 메소드 실행 시
    def run(self):
        # print("child process", id(self))

        args, w, h, e = self.init_model()
        print("[Time]", time.time() - self.start_time)

        while True:
            print("[System] Run motion")
            image = self.image_queue.get()
            if type(image) is str:
                print("[System end process]")
                break
            else:
                self.motionTracking(args, e, w, h, image)

    def motionTracking(self, args, e, w, h, decimg):
        humans = e.inference(decimg, resize_to_default=(w > 0 and h > 0),
                             upsample_size=args.resize_out_ratio)
        y1 = [0.0]
        y = 0
        image = TfPoseEstimator.draw_humans(decimg, humans, imgcopy=False)
        for human in humans:
            for i in range(len(humans)):
                try:
                    a = human.body_parts[0]
                    x = a.x * image.shape[1]
                    y = a.y * image.shape[0]
                    y1.append(y)
                    # print(y1[-2])
                except:
                    pass
                if ((y - y1[len(y1) - 2]) > 30):
                    # print("fall", i + 1)
                    pass
                # send_data={"name" :"fall"}
                # r=requests.post("http://127.0.0.1:5000/http",json=send_data)
        """
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        """
        cv2.imshow('tf-pose-estimation result', image)
        _ = 0xFF & cv2.waitKey(1)

    def init_model(self):
        print("[System] model init")
        """
        parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
        parser.add_argument('--resize', type=str, default='0x0',
                            help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
        parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                            help='if provided, resize heatmaps before they are post-processed. default=1.0')

        parser.add_argument('--model', type=str, default='mobilenet',
                            help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
        parser.add_argument('--show-process', type=bool, default=False,
                            help='for debug purpose, if enabled, speed for inference is dropped.')

        parser.add_argument('--tensorrt', type=str, default="False",
                            help='for tensorrt process.')
        args = parser.parse_args()
        w, h = model_wh(args.resize)
        print(parser)
        if w > 0 and h > 0:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h),
                                trt_bool=str2bool(args.tensorrt))
        else:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368),
                                trt_bool=str2bool(args.tensorrt))
        print("************************")
        """
        parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
        parser.add_argument('--camera', type=int, default=0)

        parser.add_argument('--resize', type=str, default='0x0',
                            help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
        parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                            help='if provided, resize heatmaps before they are post-processed. default=1.0')

        parser.add_argument('--model', type=str, default='mobilenet_thin',
                            help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
        parser.add_argument('--show-process', type=bool, default=False,
                            help='for debug purpose, if enabled, speed for inference is dropped.')

        parser.add_argument('--tensorrt', type=str, default="False",
                            help='for tensorrt process.')
        args = parser.parse_args()

        print('[System] initialization %s : %s' % (args.model, get_graph_path(args.model)))
        w, h = model_wh(args.resize)
        # print('[System] n %s : %s' % (args.model, get_graph_path(args.model)))
        if w > 0 and h > 0:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), trt_bool=str2bool(args.tensorrt))

        else:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), trt_bool=str2bool(args.tensorrt))
        print("[System] End model")
        return args, w, h, e
