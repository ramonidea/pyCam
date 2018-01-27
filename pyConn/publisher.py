#!/usr/bin/env python
from openni2_device_init import visionsensor
import rospy
from std_msgs.msg import String
import time
import rospy
import cv2
import numpy as np
import blosc
import scipy.ndimage
import thread


def keyboard_thread(list_a):
    raw_input()
    list_a.append(True)


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
        list_a = []
        thread.start_new_thread(keyboard_thread, (list_a,))
        while not rospy.is_shutdown():
            if not list_a:

                #rgb = zoom(self.device.getRgb(), [0.5,0.5,1])
                #depth = scipy.ndimage.interpolation.zoom(self.device.getDepth2Int8(), [0.5,0.5])
                rgb = self.device.getRgb()
                depth = self.device.getDepth2Int8().reshape(480,640,1)
                tarray = np.dstack((rgb,depth))

                self.rgbd.publish(blosc.pack_array(tarray))

                #d4d = self.device.getDepth2Gray()

                #self.node_c.publish(self.device.getRgbd())
                #cv2.imshow("depth",d4d)
                #cv2.waitKey(1)&255

            else:
                break
        self.device.rgb_stream.stop()
        self.device.depth_stream.stop()





if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
        rgbd.publishFrame()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")

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
