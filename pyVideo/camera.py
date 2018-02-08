import cv2
from openni2_device_init import visionsensor
import numpy as np
from PIL import Image
from io import BytesIO
import time
import zlib


class VideoCamera(object):
    def __init__(self, cam):
        self.cam = cam
        if cam == "rgb":
            self.device = visionsensor()
            self.device.createColor() # default 640*480*30fps
            self.device.startColor()
        else:
            self.device = visionsensor()
            self.device.createDepth()
            self.device.startDepth()
        time.sleep(1)


    def __del__(self):
        if self.cam =="rgb":
            self.device.stopColor()
        else:
            self.device.stopDepth()

    def get_frame(self):
        if(self.cam == "rgb"):
            rgb = self.device.getRgb()
        #img = Image.fromarray(rgb)
        #fpath =BytesIO()
        #img.save(fpath, quality = 75, format = "JPEG")
        #fpath.seek(0)
            ret, jpeg = cv2.imencode('.jpg', rgb)

            return jpeg.tobytes()#fpath.getvalue()
        else:
            depth = self.device.getDepth2Int8()
            return zlib.compress(depth.tostring()).encode()
