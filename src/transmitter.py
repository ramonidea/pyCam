from utils import *
import time
from multiprocessing import Pool
from socket import *


def transmit_image(port,hostAddr, data_queue):
    def prepare_data(_data, _count):
        return str(_count) + "f" + _data
    s = socket(AF_INET, SOCK_STREAM)
    while True:
        count, data = data_queue.pop()
        data = prepare_data(data, count)
        try:
            s.connect((hostAddr, port))
        except error:
            print("Please run the receiver function first before run the transmitter function.")
            time.sleep(0.1)
        s.sendto(data, (hostAddr, port))
    s.close()


def get_frame(data_queue):
    count = 0
    while True:
        data_queue.push(camera.get_compressed_frame(), count)
        count += 1


if __name__ == "__main__":
    data_queue = DataQueue()
    camera = VisionSensor(mock=True)
    camera.start_camera()
    camera.create_streams()
    camera.sync()
    while True:
        camera_pool = Pool(processes=1)
        camera_pool.apply(get_frame, data_queue)
        camera_pool.close()

        p = Pool(processes=30)
        ret = [p.apply_async(transmit_image, (6000 + x, '0.0.0.0', data_queue)) for x in range(10)]
        p.close()
        camera_pool.join()
        p.join()

