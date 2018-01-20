#!/usr/bin/env python
import time
import cv2
import numpy as np
import rospy
from std_msgs.msg import String
import blosc

count = 0
lasttime = 0

r = np.zeros((480*640,1),dtype=np.uint8)
g = np.zeros((480*640,1),dtype=np.uint8)
b = np.zeros((480*640,1),dtype=np.uint8)
d = np.zeros((480*640),dtype=np.uint8)

rb = False
gb = False
bb = False
db = False


def parseData(data):
    #print(len(data))
    data = blosc.decompress(data)
    #data = np.split(data,[921600])

    data = np.fromstring(data, dtype = np.uint8).reshape(480,640)
    #color = np.fromstring(data[0], dtype=np.uint8).reshape(480,640,3)
    #depth = np.fromstring(data[1], dtype=np.uint8).reshape(480,640)
    #d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

    #d4d = frame
    #d4d = np.uint8(frame.astype(float) * 255 / 2 ** 12 - 1)
    return data
    #return np.hstack((color,d4d))


def callback(data):
    # print(len(data.data))

    global count, lasttime
    #parseData(data.data)
    #cv2.waitKey(1) & 255
    #cv2.imshow("RGBD", parseData(data.data))
    print(len(parseData(data.data)))


'''
    if (int(round(time.time() * 1000)) - lasttime > 5000):
        lasttime = int(round(time.time() * 1000))
        print("Average FPS:" + str(count / 5.0))
        count = 0
    count += 1
    '''

def listener():
    global count, lasttime
    print("Start")
    rospy.init_node('Ramon', anonymous=False)
    print("Finish initialize ROS node")
    lasttime = int(round(time.time() * 1000))
    rospy.Subscriber("/RGBC", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()



'''def callbackr(data):
    global rb, gb, bb, db, r,g,b,d
    r = parseData(data.data)
    rb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackg(data):
    global rb, gb, bb, db, r,g,b,d
    g = parseData(data.data)
    gb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackb(data):
    global rb, gb, bb, db, r,g,b,d
    b = parseData(data.data)
    bb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackd(data):
    global rb, gb, bb, db, r,g,b,d
    d = parseData(data.data)
    d = 255 - cv2.cvtColor(d,cv2.COLOR_GRAY2RGB)
    db = True
    #if(rb and gb and bb and db):
        #show_image()
def show_image():
    global rb, gb, bb, db, r,g,b,d, count, lasttime
    rb = False
    gb = False
    bb = False
    db = False
    cv2.waitKey(1) & 255
    rgb = np.dstack((r,g,b))
    cv2.imshow("RGBD", np.hstack((rgb, d)))
    '''
