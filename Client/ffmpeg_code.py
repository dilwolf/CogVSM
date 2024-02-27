
# from mlmodule import detect
parser = argparse.ArgumentParser(
    description='Example streaming ffmpeg numpy processing')
parser.add_argument('in_filename', help='Input filename')
parser.add_argument('out_filename', help='Output filename')
parser.add_argument(
    '--dream', action='store_true', help='Use DeepDream frame processing (requires tensorflow)')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_video_size(filename):
    logger.info('Getting video size for {!r}'.format(filename))
    probe = ffmpeg.probe(filename)
    video_info = next(s for s in probe['streams']
                      if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    return width, height


def start_ffmpeg_process1(in_filename):
    logger.info('Starting ffmpeg process1')
    args = (
        ffmpeg
        .input(in_filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .compile()
    )
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def start_ffmpeg_process2(out_filename, width, height):
    logger.info('Starting ffmpeg process2')
    args = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        .output(out_filename, pix_fmt='yuv420p')
        .overwrite_output()
        .compile()
    )
    return subprocess.Popen(args, stdin=subprocess.PIPE)


def read_frame(process1, width, height):
    logger.debug('Reading frame')

    # Note: RGB24 == 3 bytes per pixel.
    frame_size = width * height * 3
    in_bytes = process1.stdout.read(frame_size)
    if len(in_bytes) == 0:
        frame = None
    else:
        assert len(in_bytes) == frame_size
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
    return frame


def process_frame_simple(frame):
    '''Simple processing example: darken frame.'''
    return frame * 0.3


def write_frame(process2, frame):
    logger.debug('Writing frame')
    process2.stdin.write(
        frame
        .astype(np.uint8)
        .tobytes()
    )


def run(in_filename, out_filename, process_frame):
    width, height = get_video_size(in_filename)
    process1 = start_ffmpeg_process1(in_filename)
    process2 = start_ffmpeg_process2(out_filename, width, height)
    while True:
        in_frame = read_frame(process1, width, height)
        if in_frame is None:
            logger.info('End of input stream')
            break

        logger.debug('Processing frame')
        out_frame = process_frame(in_frame)
        write_frame(process2, out_frame)

    logger.info('Waiting for ffmpeg process1')
    process1.wait()

    logger.info('Waiting for ffmpeg process2')
    process2.stdin.close()
    process2.wait()

    logger.info('Done')


process_frame = process_frame_simple
run("sample_vids\longvid.m4v", "output\demovid1.mp4", process_frame)

# def main1():
#     print("started inference")
#     detect.run(weights="weights/yolov5l.pt",
#                source="sample_vids/longvid.m4v",
#                view_img=True,
#                save_txt=True,
#                project="output",

#                )
#     print("finished inference")


# def main2():
#     print("started inference")
#     detect.run(weights="weights/yolov5l.pt",
#                source="sample_vids/shortvid.avi",
#                view_img=True,
#                save_txt=True,
#                project="output"
#                )
#     print("finished inference")


# # def server_main():
# #     # Socket Create
# #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     host_name = socket.gethostname()
# #     host_ip = socket.gethostbyname(host_name)
# #     print('HOST IP:', host_ip)
# #     port = 9999
# #     socket_address = (host_ip, port)

# #     # Socket Bind
# #     server_socket.bind(socket_address)

# #     # Socket Listen
# #     server_socket.listen(5)
# #     print("LISTENING AT:", socket_address)

# #     # Socket Accept
# #     while True:
# #         client_socket, addr = server_socket.accept()
# #         print('GOT CONNECTION FROM:', addr)
# #         if client_socket:
# #             vid = cv2.VideoCapture(
# #                 r"D:\2_Professional\3_Python\6_PyPrac\streamObjDet\sample_vids\shortvid.avi")

# #             while (vid.isOpened()):
# #                 img, frame = vid.read()
# #                 frame = imutils.resize(frame, width=512)
# #                 a = pickle.dumps(frame)
# #                 message = struct.pack("Q", len(a))+a
# #                 time.sleep(0.1)
# #                 client_socket.sendall(message)
# #                 try:
# #                     # send message or data frames to client
# #                     client_socket.sendall(message)
# #                 except Exception as e:
# #                     print(e)
# #                     raise Exception(e)

# #                 cv2.imshow('TRANSMITTING VIDEO', frame)
# #                 key = cv2.waitKey(1) & 0xFF
# #                 if key == ord('q'):
# #                     client_socket.close()


# x = threading.Thread(target=main1, name='inference_thread').start()
# x = threading.Thread(target=main2, name='inference_thread').start()
# # x = threading.Thread(target=server_main, name='server_thread').start()

# # for ip camera use -
# # rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
