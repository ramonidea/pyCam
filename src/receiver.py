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
    s.bind((host, remoteport))
    print((host, remoteport))
    while True:
        s.listen(5)
        conn, addr = s.accept()
        print(addr)
        arr1 = b""
        digit = int(conn.recv(8))
        while True:
            if digit <= 0:
                break
            rawdata = conn.recv(BUFSIZE)
            print(len(rawdata))
            arr1 += rawdata
            digit -= len(rawdata)
        print(222)
        conn.sendall("DONE")
        print("PICTURE: "+ arr1[0:arr1.index(b'f')])
        data_queue.push(int(arr1[0:arr1.index(b'f')]), arr1[arr1.index(b'f')+1:])
        s.close()

if __name__ == '__main__':

    while True:
        show = Process(target=display)
        show.start()
        p = Pool(processes=30)
        ret = [p.apply_async(worker, (50000 + x, "0.0.0.0")) for x in range(10)]
        p.close()
        show.join()
        p.join()



            #cv2.imshow('image',cv2.imdecode(np.frombuffer(result[1], np.uint8), -1))
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break


    cv2.destroyAllWindows()