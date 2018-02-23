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
import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = 255 - cv2.cvtColor(np.asarray(depth_frame.get_data()), cv2.COLOR_GRAY2RGB)
        #depth_image = np.asarray(depth_frame.get_data())

        color_image = np.asarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_image))
        print(images.shape)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()
