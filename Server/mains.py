import warnings

from modules.MultiSocket import create_thread
import socket

warnings.filterwarnings(action="ignore")

if __name__ == '__main__':
    # TODO: Creating a queue to be shared between the data manager and the process manager
    # TODO: run data manager
    # TODO: run process manager
    # socket connection part
    HOST, PORT = ('', 9998) #Put your ip address
    HOST_PORT = (HOST, PORT)
    clients_limit = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind(HOST_PORT)
    print('Socket bind complete')
    s.listen(clients_limit)
    print('Socket now listening {} clients'.format(clients_limit))

    create_thread(s)

