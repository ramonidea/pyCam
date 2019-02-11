from socket import *
import cv2
import numpy as np
import time
from multiprocessing import Pool, Process
from utils import *
data = []
data_queue = DataQueue()


def display():
    global data,  data_queue
    while True:
        if len(data_queue) > 0:
            key, image = data_queue.pop()
            data.append(image)
            print(key)


def worker(remoteport, host):
    global data_queue
    BUFSIZE = 10000
    s = socket(AF_INET, SOCK_STREAM)
    while True:
        s.bind((host, remoteport))
        s.listen(1)
        conn, addr = s.accept()
        arr1 = b""
        while True:
            rawdata = conn.recv(BUFSIZE)
            if not rawdata:
                break
            arr1 += rawdata
        s.sendto("DONE",addr)
        print("PICTURE: "+ arr1[0:arr1.index(b'f')])
        data_queue.push(int(arr1[0:arr1.index(b'f')]), arr1[arr1.index(b'f')+1:])
        s.close()

if __name__ == '__main__':

    while True:
        show = Process(target=display)
        show.start()
        p = Pool(processes=30)
        ret = [p.apply_async(worker, (20000 + x, "0.0.0.0")) for x in range(10)]
        p.close()
        show.join()
        p.join()



            #cv2.imshow('image',cv2.imdecode(np.frombuffer(result[1], np.uint8), -1))
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break


    cv2.destroyAllWindows()