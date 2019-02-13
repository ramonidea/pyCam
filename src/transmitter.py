from utils import *
import time
from multiprocessing import Pool
from socket import *

data_queue = DataQueue()

def transmit_image(port,hostAddr,cur_port):
    global data_queue
    def prepare_data(_data, _count):
        data  = format(len(_data), '08d')
        data += str(_count) + "f" + _data
        return data

    print((hostAddr, port))
    s = socket(AF_INET, SOCK_STREAM)
    while True:
        if len(data_queue)>0:
            count, data = data_queue.pop()
            s.connect((hostAddr, port))

            data = prepare_data(data, count)
            print(len(data))
            s.sendall(data)
            print(11)
            data = s.recv(100)
            print(data)
            s.close()


def get_frame():
    global data_queue
    count = 0
    while True:
        temp = camera.get_compressed_frame()
        data_queue.push(temp[0], temp[2])
        count += 1


if __name__ == "__main__":

    camera = VisionSensor(mock=True)
    camera.start_camera()
    camera.create_streams()
    camera.sync()
    while True:
        camera_pool = Process(target=get_frame)
        camera_pool.start()
        p = Pool(processes=30)
        ret = [p.apply_async(transmit_image, (50000 + x, '0.0.0.0', 10000 + x)) for x in range(10)]
        p.close()
        camera_pool.join()
        p.join()

