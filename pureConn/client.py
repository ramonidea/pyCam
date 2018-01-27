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

IP_SERVER = "69.91.157.166"
PORT_SERVER = 953
TIMEOUT_SOCKET = 10
SIZE_PACKAGE = 4096

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB


if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.settimeout(TIMEOUT_SOCKET)
    connection.connect((IP_SERVER, PORT_SERVER))
    count = 0
    lasttime = int(round(time.time() * 1000))

    while True:
        try:
            fileDescriptor = connection.makefile(mode='rb')
            result = fileDescriptor.readline()
            fileDescriptor.close()
            result = base64.b64decode(result)

            data = blosc.unpack_array(result)
            data = np.dsplit(data,[3])
            color = data[0]
            depth = data[1].reshape(240,320)
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
