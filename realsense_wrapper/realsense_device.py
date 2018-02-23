#!/usr/bin/env python3.5

# Depedency:
# Need to follow the instruction here to set up the machine and install python wrapper
# https://github.com/IntelRealSense/librealsense
#
#
# git clone https://github.com/IntelRealSense/librealsense
# cd librealsense
# mkdir build
# cd build
# cmake ../ -DBUILD_PYTHON_BINDINGS=TRUE
# make -j4
# sudo make install #Optional if you want the library to be installed in your system
#
#

class visionsensor:
    def __init__(self, x = 640, y = 480, fpd = 30, rgb = True, depth = True):
        self.x = x
        self.y = y
        self.fps = fps
        self.rgb = rgb
        self.depth = depth


    #Start the Color Camera
    def startColor(self):


    #Start the Depth Camera
    def startDepth(self):


    #Stop the Depth Camera
    def stop(self):


    #Initialize color camera (default 640 * 360 * 30fps)
    def createColor(self):


    #Initialize the Depth camera (default 640*360*30fps)
    def createDepth(self):

    #Enable the depth and color sync (un after initalized both cameras, before running them)
    def sync(self):

    #Return / Initalize self.rgb as the numpy array (uint8 3L 640 * 480 * 3 * uint8)
    def getRgb(self):

    #Return self.dmap as the numpy array (1L uint16, 0 - 2**12-1)
    def getDepth(self):





    def getDepth2Int8(self):
