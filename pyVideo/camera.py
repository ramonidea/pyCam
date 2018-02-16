import cv2
from openni2_device_init import visionsensor
import numpy as np
from PIL import Image
from io import BytesIO
import time
import zlib


class VideoCamera(object):
    def __init__(self,x = 640, y = 480, fpd = 30, rgb_mirror = False,
            depth_mirror = False, rgb = True, depth = True):
        self.device = visionsensor()
        self.device.createColor() # default 640*480*30fps
        self.device.startColor()
        self.device.createDepth()
        self.device.startDepth()
        time.sleep(1)


    def __del__(self):
        self.device.stop()

    def get_frame(self):
        rgb = self.device.getRgb()
        #img = Image.fromarray(rgb)
        #fpath =BytesIO()
        #img.save(fpath, quality = 75, format = "JPEG")
        #fpath.seek(0)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
        ret, jpeg = cv2.imencode('.jpg', rgb, encode_param)
        depth = self.device.getDepth()
        return jpeg.tobytes() , zlib.compress(depth)
