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
import rospy
from sensor_msgs.msg import CompressedImage,CameraInfo
from std_msgs.msg import String

#To parse the command line arguments
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

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

def retriveCameraInfo(ip, port):
    info = urlopen("http://"+ip+':'+port+'/camera_info')
    result = str(info.read(1024)).split('-')
    x = int(result[0][1:])
    y = int(result[1][1:])
    fps = int(result[2][3:])
    return x,y,fps


if __name__ == '__main__':
    #Global Variables

    ip = ''
    port = ''
    videoX = 640
    videoY = 480
    videoFps = 30
    rgb = True
    depth = True

    myargs = getopts(argv)
    try:
        if "-ip" in myargs:
            ip = myargs["-ip"]
        if "-port" in myargs:
            port = myargs["-port"]
    except Exception, e:
        print(e.message)

    if ip == "" or port == '':
        print("Please Enter IP Address of the local machine")
    else:
        print("Remote Joule is set to "+ip+':' +str(port))
        print("Init ROS")
        rgb_pub = rospy.Publisher("/Camera/rgb",CompressedImage,queue_size=30)
        print("/Camera/rgb is published, (CompressedImage)")
        depth_pub = rospy.Publisher("/Camera/depth",CompressedImage,queue_size=30)
        print("/Camera/depth is published, (CompressedImage)")
        camera_info = rospy.Publisher("/Camera/camera_info",CameraInfo,queue_size=30)
        print("/Camera/camera_info is published, (camera_info)")
        rospy.init_node("Joule", anonymous=False)
         while not rospy.is_shutdown():
            try:
                if camera_info.get_num_connections() > 0:
                    videoX, videoY, videoFps = retriveCameraInfo(ip,port)


                if depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
                    video = urlopen("http://"+ip+":"+port+"/video_feed")
                    while depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
                        rgb,depth = getFrame(video)
                        rgb = cv2.cvtColor(np.asarray(Image.open(rgb)), cv2.COLOR_RGB2BGR)

                        depth = np.fromstring(depth,dtype=np.uint16).reshape(480,640)


            except Exception,e:
                if e == KeyboardInterrupt:
                    break




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
