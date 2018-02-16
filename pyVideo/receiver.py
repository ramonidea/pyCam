try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import numpy as np
from PIL import Image
from io import StringIO
import cv2
from io import BytesIO
import time
import zlib

def getFrame(response):
    rgbData = b''
    depthData = b''
    while 1:
        temp = response.read(4096)
        a = temp.find(b'e\r\nContent-Type: image/jpeg\r\n\r\n')
        b = temp.find(b'--frame')
        if(a==-1):
            rgbData += temp
        else:
            head = temp[b+7:a]
            rgb = head.find(b'f')
            depth = head[rgb+1:]
            rgb = head[:rgb]
            rgbData = temp[a+31:]
            break
    num = int(rgb)
    left = num - (4096-a-31)
    rgbData += response.read(left)
    depthData = response.read(int(depth))
    return BytesIO(rgbData), zlib.decompress(depthData)


if __name__ == '__main__':
    video = urlopen("http://173.250.181.115:5000/video_feed")
    count = 0
    lasttime = 0
    lasttime = int(round(time.time() * 1000))
    while True:
            rgb,depth = getFrame(video)
            rgb = cv2.cvtColor(np.asarray(Image.open(rgb)), cv2.COLOR_RGB2BGR)

            depth = np.fromstring(depth,dtype=np.uint8).reshape(480,640)
            depth = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

            cv2.waitKey(1) & 255
            cv2.imshow("RGBD", np.hstack((rgb,depth)))
            if (int(round(time.time() * 1000)) - lasttime > 10000):
                lasttime = int(round(time.time() * 1000))
                print("Average FPS:" + str(count / 10.0))
                count = 0
            count += 1
