import cv2
from openni2_device_init import visionsensor
import numpy as np
from PIL import Image
from io import BytesIO
import time


class VideoCamera(object):
    def __init__(self):
        self.device = visionsensor()
        self.device.createColor() # default 640*480*30fps
        #self.device.sync()
        self.device.startColor()
        time.sleep(1)

    def __del__(self):
        self.device.stopColor()

    def get_frame(self):
        rgb = self.device.getRgb()
        #img = Image.fromarray(rgb)
        #fpath =BytesIO()
        #img.save(fpath, quality = 75, format = "JPEG")
        #fpath.seek(0)
        ret, jpeg = cv2.imencode('.jpg', rgb)

        return jpeg.tobytes()#fpath.getvalue()
