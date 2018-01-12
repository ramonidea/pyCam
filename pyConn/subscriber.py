#!/usr/bin/env python
import time
import zlib

import cv2
import numpy as np
import rospy
from std_msgs.msg import String, UInt16MultiArray
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge

count = 0
lasttime = 0


def parseData(data):
    data = zlib.decompress(data).split(" ")
    data = [int(i) for i in data]

    # frame = zlib.decompress(data)
    frame = np.asarray(data, dtype=np.uint8).reshape(480, 640)
    d4d = frame
    d4d = np.uint8(frame.astype(float) * 255 / 2 ** 12 - 1)
    d4d = 255 - cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
    return d4d


'''  
br = CvBridge()

  #rospy.loginfo(rospy.get_caller_id() + "I heard")
  cv_image = br.imgmsg_to_cv2(data, desired_encoding="passthrough")

'''
def callback(data):
    # print(len(data.data))

    global count, lasttime

    #cv2.waitKey(1) & 255
    #cv2.imshow("Depth", parseData(data.data))

    if (int(round(time.time() * 1000)) - lasttime > 5000):
        lasttime = int(round(time.time() * 1000))
        print("Average FPS:" + str(count / 5.0))
        count = 0
    count += 1


def listener():
    global count, lasttime
    print("Start")
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=False)
    print("Finish initialize")
    lasttime = int(round(time.time() * 1000))
    rospy.Subscriber("/camera/depth_compressed/image_compressed", CompressedImage, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
