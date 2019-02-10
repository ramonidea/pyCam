from socket import *
import cv2
import numpy
from multiprocessing import Pool

def worker(remoteport, host, port):
        print(remoteport)
        BUFSIZE = 300000
        s = socket(AF_INET, TCP_NODELAY)
        s.bind(('', port))
        s.listen(5)
        conn, (host, remoteport) = s.accept()
        arr1 = b""
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            arr1 += data
        return int(arr1[0:arr1.index(b'f')]), arr1[arr1.index(b'f')+1:]

if __name__ == '__main__':
    while True:
        p = Pool(processes=30)
        ret = [p.apply_async(worker, (5000 + x, '192.168.177', 9000 + x)) for x in range(10)]
        p.close()
        p.join()
        for i in ret:
            print(ret[0])

            cv2.imshow('image',cv2.imdecode(np.frombuffer(ret[1], np.uint8), -1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    cv2.destroyAllWindows()