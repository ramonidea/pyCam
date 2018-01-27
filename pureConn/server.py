#!/usr/bin/env python
'''
The code will run on the Transmitter side (Joule)
will stream the video data from the camera
Pure Python Socket program, without using ROS platform
Purpose: To test the transmission rate and latency vs runing on ROS
'''
from openni2_device_init import visionsensor
import time
import json
import socket
import base64
import numpy as np
import blosc
from threading import Thread


SERVER_IP = "69.91.157.166"
SERVER_PORT = 953
MAX_NUM_CONNECTIONS = 5


class ConnectionPool(Thread):

    def __init__(self, ip_, port_, conn_):
        Thread.__init__(self)
        self.ip = ip_
        self.port = port_
        self.conn = conn_
        print "[+] New server socket thread started for " + self.ip + ":" + \
            str(self.port)
        self.device = visionsensor()
        self.initDevice()


    def initDevice(self):
        self.device.createColor()
        self.device.createDepth()
        self.device.sync()
        self.device.startColor()
        self.device.startDepth()

    def getData(self):
        rgb = self.device.getRgb()
        depth = self.device.getDepth2Int8()
        tarray = np.dstack((rgb,depth))
        return tarray

    def run(self):
        try:
            while True:
                data = blosc.pack_array(self.getData())
                self.conn.sendall(base64.b64encode(data) + '\r\n')
        except Exception, e:
            print "Connection lost with " + self.ip + ":" + str(self.port) + \
                  "\r\n[Error] " + str(e.message)
        self.conn.close()



if __name__ == '__main__':


    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((SERVER_IP, SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = ConnectionPool(ip, port, conn, camera)
        thread.start()
    connection.close()
