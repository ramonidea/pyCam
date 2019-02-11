from socket import *
import cv2
import numpy as np
import time
from multiprocessing import Pool

data = []


def display(data_queue):
    global data
    while True:
        if len(data_queue) > 0:
            key, image = data_queue.pop()
            data.append(image)
            print(key)




def worker(remoteport, host, data_queue):
    while True:
        print(remoteport, host)
        BUFSIZE = 300000
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((host, remoteport))
        s.listen(1)
        conn, addr = s.accept()
        arr1 = b""
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            arr1 += data
        data_queue.push(int(arr1[0:arr1.index(b'f')]), arr1[arr1.index(b'f')+1:])

if __name__ == '__main__':
    data_queue = DataQueue()
    while True:
        show = Pool(processes=1)
        show.close()

        p = Pool(processes=30)
        ret = [p.apply_async(worker, (6000 + x, "0.0.0.0",data_queue)) for x in range(10)]
        p.close()
        show.join()
        p.join()



            #cv2.imshow('image',cv2.imdecode(np.frombuffer(result[1], np.uint8), -1))
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break


    cv2.destroyAllWindows()