#!/usr/bin/env python31
import cv2
from realsense_device import visionsensor
import numpy as np
from PIL import Image
from io import BytesIO
import time
import zlib


class VideoCamera(object):
    def __init__(self,x = 640, y = 360, fps= 30):
        self.device = visionsensor(x = x, y = y, fps = fps)

        self.device.createStreams()


        time.sleep(1)


    def __del__(self):
        self.device.stop()

    def start_camera(self):
        self.device.startCamera()
        self.device.sync()

    def get_frame(self, rgb_compress = 75):
        rgb, depth = self.device.getFrame()
        #img = Image.fromarray(rgb)
        #fpath =BytesIO()
        #img.save(fpath, quality = 75, format = "JPEG")
        #fpath.seek(0)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), rgb_compress]
        ret, jpeg = cv2.imencode('.jpg', rgb, encode_param)
        jpeg = jpeg.tobytes()
        depth = zlib.compress(depth)
        return jpeg, depth