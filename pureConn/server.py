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
from socket import *
import base64
import numpy as np
import blosc
import zlib
from threading import Thread
from PIL import Image
from io import BytesIO

SERVER_IP = "69.91.157.166"
SERVER_PORT = 1080
MAX_NUM_CONNECTIONS = 5


class ConnectionPool(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.BUFSIZE = 10000
        self.hostAddr = "173.250.181.211"
        self.PORT = 3030

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
        depth = self.device.getDepth2Gray(self.device.getDepth2Int8())
        #tarray = np.dstack((rgb,depth))
        return rgb, depth

    def send(self,data):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.hostAddr, self.PORT))
        self.s.sendto(data,(self.hostAddr,self.PORT))
        #self.adata = len(data)
        #print("Pre:"+str(self.ndata)+" After: "+str(self.adata)+" rate"+str(round(self.adata*1.0/self.ndata*100)))
        self.s.close()

    def run(self):
        try:
            while True:

                #PIL same to JPEG and read the byte array
                rgb, depth = self.getData()
                img = Image.fromarray(rgb)
                img1 = Image.fromarray(depth)
                fpath =BytesIO()
                img.save(fpath, quality = 75, format = "JPEG")
                #img.save("rgb.jpg",quality = 75)
                fpath.seek(0)
                self.send(fpath.getvalue())
                dpath = BytesIO()
                img1.save(dpath, quality = 75, format = "JPEG")
                dpath.seek(0)
                self.send(dpath.getvalue())
                #with open("depth.jpg") as f:
                #    depth = f.read()





                '''
                Intra-Frame Compression
                data = self.getData().tostring()
                self.ndata = len(data)
                data = blosc.compress(data)
                self.send(data)
                '''
        except Exception, e:
            print "[Error] " + str(e.message)



if __name__ == '__main__':
        thread = ConnectionPool()
        thread.start()
