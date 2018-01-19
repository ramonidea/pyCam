#!/usr/bin/env python
import time
import cv2
import numpy as np
import rospy
from std_msgs.msg import String
import blosc

count = 0
lasttime = 0


def callback(data):
    # print(len(data.data))

    global count, lasttime

    cv2.waitKey(1) & 255
    cv2.imshow("Depth", blosc.unpack_array(data.data))

    if (int(round(time.time() * 1000)) - lasttime > 5000):
        lasttime = int(round(time.time() * 1000))
        print("Average FPS:" + str(count / 5.0))
        count = 0
    count += 1


def listener():
    global count, lasttime
    print("Start")
    rospy.init_node('Ramon', anonymous=False)
    print("Finish initialize ROS node")
    lasttime = int(round(time.time() * 1000))
    rospy.Subscriber("/Depth", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
