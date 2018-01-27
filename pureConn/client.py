#!/usr/bin/env python
'''
The code will run on the receiver side
will receive the data from the stream server
Pure Python Socket program, without using ROS platform
Purpose: To test the transmission rate and latency vs runing on ROS
'''
import cv2
import socket
import base64
import numpy as np
import blosc
import time

IP_SERVER = "69.91.157.166"
PORT_SERVER = 1080
TIMEOUT_SOCKET = 10
SIZE_PACKAGE = 4096

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB


if __name__ == '__main__':
    PORT = 5000  # default 5000 for both sides
    s.bind(('', PORT))
    s.listen(5)
    BUFSIZE = 8192  # should be 2^n
    s = socket(AF_INET, TCP_NODELAY)

    count = 0
    lasttime = int(round(time.time() * 1000))

    while True:
        try:
            conn, (host, remoteport) = self.s.accept()
            arr1 = b""
            while True:
                data = conn.recv(self.BUFSIZE)
                if not data:
                    break
                arr1 += data

            data = blosc.unpack_array(result)
            #data = np.fromstring(result, dtype=np.uint8).reshape(480,640,4)
            data = np.dsplit(data,[3])
            color = data[0]
            depth = data[1].reshape(480,640)
            d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
            cv2.imshow('Depth || Color', np.hstack((rgb,d4d)))


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if (int(round(time.time() * 1000)) - lasttime > 5000):
                lasttime = int(round(time.time() * 1000))
                print("Average FPS:" + str(count / 5.0))
                count = 0
            count += 1

        except Exception as e:
            print "[Error] " + str(e)

    connection.close()
