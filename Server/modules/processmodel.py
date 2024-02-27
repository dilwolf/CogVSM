import tensorflow as tf
import numpy as np
from threading import Thread

tf.config.set_visible_devices([], 'GPU')
# tf.compat.v1.disable_eager_execution()
config = tf.compat.v1.ConfigProto() #device_count = {'GPU': 0}
config.gpu_options.allow_growth = False
graph = tf.compat.v1.get_default_graph()
first_session = tf.compat.v1.Session(config=config)
with graph.as_default(), first_session.as_default():
    with graph.as_default():
        with tf.device('CPU:0'):
            model = tf.keras.models.load_model('/home/dilshod/Cog1/tf-pose-estimation/modules/lstm_model/model1.h5', compile=False)
print(model.summary())


def make_prediction(m):
    WINDOW_SIZE, alpha, theta = 5, 0.9, 3
    forecast_ewma, actual_values, forecast_values, theta_values, arr_of_num = [0], [], [], [], [1,1,1,1,1]
    arr_of_num.append(m)
    if len(arr_of_num)>WINDOW_SIZE:
        arr_of_num = arr_of_num[1:]
    if len(arr_of_num)==WINDOW_SIZE:
        actual = arr_of_num[-1]
        with graph.as_default(), first_session.as_default():
            forecast = model.predict(np.array(arr_of_num[-WINDOW_SIZE:]).reshape(1, WINDOW_SIZE, 1))[0][0]
            forecast_values.append(forecast)
            a = alpha * forecast + (1 - alpha) * forecast_values[-1]
            theta += 1 if a > 0.5 else -1
            theta = min(max(theta, 0), 2)
            theta_values.append(theta)
            forecast_ewma.append(a)
            return actual, forecast #theta


# TODO: if "class LSTM(Thread):" does not work, you can refer to test.py
