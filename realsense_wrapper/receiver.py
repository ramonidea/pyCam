try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import numpy as np
import PIL.Image
from io import StringIO
import cv2
from io import BytesIO
import time
import zlib
import rospy
from sensor_msgs.msg import CompressedImage,CameraInfo, Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sys import argv

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
    print(result)
    x = int(result[1][1:])
    y = int(result[2][1:])
    print(result[3], result[4])
    return x,y


if __name__ == '__main__':
    #Global Variables

    ip = ''
    port = ''
    videoX = 640
    videoY = 360
    videoFps = 30
    rgb = True
    depth = True

    myargs = getopts(argv)
    try:
        if "-ip" in myargs:
            ip = myargs["-ip"]
        if "-port" in myargs:
            port = myargs["-port"]
    except Exception:
        print(e.message)

    if ip == "" or port == '':
        print("Please Enter IP Address of the local machine")
    else:
        print("Remote Joule is set to "+ip+':' +str(port))
        print("Init ROS")
        rgb_pub = rospy.Publisher("/Camera/rgb",CompressedImage,queue_size=30)
        print("/Camera/rgb is published, (CompressedImage)")
        depth_pub = rospy.Publisher("/Camera/depth",CompressedImage,queue_size=30)
        print("/Camera/depth is published, (Image)")
        camera_info = rospy.Publisher("/Camera/camera_info",CameraInfo,queue_size=30)
        print("/Camera/camera_info is published, (camera_info)")
        rospy.init_node("Joule", anonymous=False)
        while not rospy.is_shutdown():
            bridge = CvBridge()
                #if camera_info.get_num_connections() > 0:
            videoX, videoY = retriveCameraInfo(ip,port)
            info_msg = CameraInfo()
            info_msg.height = videoY
            info_msg.width = videoX
            print("Finish the camera Info")
            #TODO: Need to add other parameters for the message
            #camera_info.publish(info_msg)

        #if depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
            video = urlopen("http://"+ip+":"+port+"/video_feed")
            while 1:#depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
                rgb,depth = getFrame(video)
                rgb = cv2.cvtColor(np.asarray(PIL.Image.open(rgb)), cv2.COLOR_RGB2BGR)

                rgb_msg = CompressedImage()
                rgb_msg.header.stamp = rospy.Time.now()
                rgb_msg.format = "jpeg"
                rgb_msg.data = rgb.tostring()
                # Publish new image
                #rgb_pub.publish(rgb_msg)



                depth = np.fromstring(depth,dtype=np.uint8).reshape(videoY,videoX)
                depth = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
                cv2.imshow('rgbd', np.hstack((rgb,depth)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                '''

                try:
                    depth_pub.publish(bridge.cv2_to_imgmsg(depth, "bgr8"))
                except CvBridgeError as e:
                    print(e)
                    '''
