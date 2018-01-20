#!/usr/bin/env python
from openni2_device_init import visionsensor
import rospy
from std_msgs.msg import String
import time
import rospy
import cv2
import numpy as np
import blosc
import sys
import pickle


class RgbdPublisher:
    def __init__(self):
        self.device = visionsensor()
        self.device.createDepth() # default 640*480*30fps
        self.device.createColor() # default 640*480*30fps
        self.device.sync()
        self.device.startColor()
        self.device.startDepth()

        self.RosInit() #init the cameras and ros node


    def RosInit(self):
        #self.depth = rospy.Publisher('Depth',String, queue_size=30)
        self.rgbd = rospy.Publisher('RGBD', String, queue_size=30)
        rospy.init_node("Joule", anonymous=False)

    def publishFrame(self):
      #while True:
     #self.temp = np.zeros((480*640*4),dtype=np.uint8)
      while not rospy.is_shutdown():



        #data = self.device.getRgbd()
        #data = self.device.getDepth2Int8

        #self.rgbd.publish(blosc.pack_array(data))
        #f.write(str(data))


        #self.rgbd.publish(blosc.compress(tarray.tostring()))


        #d4d = self.device.getDepth2Gray()

        #self.node_c.publish(self.device.getRgbd())
        #cv2.imshow("depth || Color",np.hstack((rgb,d4d)))
        #cv2.waitKey(1)&255
      self.device.rgb_stream.stop()
      self.device.depth_stream.stop()


      '''
      Seperate to multiple topics
rgb = self.device.getRgb()
r,g,b = np.split(rgb,3, axis=2)
r = np.squeeze(r)
g = np.squeeze(g)
b = np.squeeze(b)
d = self.device.getDepth2Int8()
#tarray = np.append(rgb,depth)
self.r.publish(blosc.compress(r.tostring()))
self.g.publish(blosc.compress(g.tostring()))
self.b.publish(blosc.compress(b.tostring()))
self.d.publish(blosc.compress(d.tostring()))

      '''


if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
        rgbd.publishFrame()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")
