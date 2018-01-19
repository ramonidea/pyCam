#!/usr/bin/env python
from openni2_device_init import visionsensor
import rospy
from std_msgs.msg import String
import time
import rospy
import cv2
import numpy as np
import blosc


class RgbdPublisher:
    def __init__(self):
        self.device = visionsensor()
        self.device.createDepth() # default 640*480*30fps
        self.device.createColor() # default 640*480*30fps
        self.device.sync()
        self.device.startDepth()
        self.device.startColor()
        self.RosInit() #init the cameras and ros node


    def RosInit(self):
        #self.depth = rospy.Publisher('Depth',String, queue_size=30)
        self.rgbd = rospy.Publisher('RGBD', String, queue_size=30)
        rospy.init_node("Joule", anonymous=False)

    def publishFrame(self):
      #while True:
     #with open("/home/test/ws/src/pyRamon/pyConn/output.txt","wb") as f:
      while not rospy.is_shutdown():

        #data = self.device.getRgbd()
        #data = self.device.getDepth2Int8

        #self.rgbd.publish(blosc.pack_array(data))
        #f.write(str(data))
        rgb = self.device.getRgb().reshape(921600)
        depth = self.device.getDepth2Int8()
        data = np.append(rgb,depth)

        self.rgbd.publish(blosc.pack_array(data))
        #d4d = self.device.getDepth2Gray()

        #self.node_c.publish(self.device.getRgbd())
        #cv2.imshow("depth || Color",np.hstack((rgb,d4d)))
        #cv2.waitKey(1)&255


if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
        rgbd.publishFrame()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")
