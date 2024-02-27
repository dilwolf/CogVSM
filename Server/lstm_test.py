import random
import time
import numpy as np
import onnxruntime as rt

sess = rt.InferenceSession('/home/dilshod/Code/Server/tf-pose-estimation/lstm_model/model1.onnx')
input_name = sess.get_inputs()[0].name



def smooth_random(start, stop, step):
    return round(random.uniform(start, stop))

WINDOW_SIZE = 5
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
        return print(f'Actual: {actual}, Forecast: {forecast}')

while True:
    # Generate a random number
    n = smooth_random(0, 10, 1)
    print("Generated number: {}".format(n))
    make_prediction(n)
    time.sleep(1)


# tf.config.set_visible_devices([], 'GPU')

# model = tf.keras.models.load_model('/home/dilshod/Cog/tf-pose-estimation/modules/lstm_model/model1.h5', compile=False)