#!/usr/bin/env python

import pyrealsense2 as rs
import numpy as np
import cv2
import time
from PIL import Image
from io import BytesIO
import zlib
from multiprocessing import Process,Value
import rospy
from sensor_msgs.msg import CameraInfo
from Queue import PriorityQueue
from multiprocessing.managers import SyncManager


class MyManager(SyncManager):
    pass


MyManager.register("PriorityQueue", PriorityQueue)  # Register a shared PriorityQueue


def Manager():
    m = MyManager()
    m.start()
    return m


class DataQueue:
    def __init__(self):
        m = Manager()
        self.data = m.PriorityQueue()
        self.cur = Value("i", -1)

    def push(self, raw_data, key):
        if key > self.cur.value:
                self.data.put((key, raw_data))

    def __len__(self):
        return self.data.qsize()

    def pop(self):

        if self.data.qsize() > 0:
            print("ttttt")
            temp = self.data.get()
            with self.cur.get_lock():
                self.cur.value = temp[0]
            return temp[0], temp[1]


def publish_camera_info(intrinsics_d, extrinsics_d, intrinsics_c, extrinsics_c, x, y):
    rospy.init_node('camera_info')
    r = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        camera_info = CameraInfo()
        camera_info.header.stamp = rospy.Time.now()
        camera_info.height = y
        camera_info.width = x


        pub.publish("hello world")
        r.sleep()


class VisionSensor:
    def __init__(self, x=640, y=360, fps=30, quality = 75, mock = False):
        self.x = x
        self.y = y
        self.fps = fps
        self.depth = None
        self.rgb = None
        self.profile = None
        self.align = None
        self.align_to = None
        self.frame_count = 0
        self.quality = quality
        self.mock = mock

        # Create a pipeline
        self.pipeline = rs.pipeline()
        # create a config
        self.config = rs.config()

    def __del__(self):
        if self.mock:
            return True
        self.pipeline.stop()

    def publish_camera_info(self):
        intrinsics_d, extrinsics_d, intrinsics_c, extrinsics_c = self.get_camera_info()
        p = Process(target=publish_camera_info, args=(intrinsics_d, extrinsics_d, intrinsics_c,
                                                      extrinsics_c, self.x, self.y))
        p.start()
        p.join()

    def get_camera_info(self):
        intrinsics_d = self.pipeline.get_active_profile().get_streams()[0].as_video_stream_profile().get_intrinsics()
        extrinsics_d = self.pipeline.get_active_profile().get_streams()[0].get_extrinsics_to(
            self.pipeline.get_active_profile().get_streams()[1])
        intrinsics_c = self.pipeline.get_active_profile().get_streams()[1].as_video_stream_profile().get_intrinsics()
        extrinsics_c = self.pipeline.get_active_profile().get_streams()[1].get_extrinsics_to(
            self.pipeline.get_active_profile().get_streams()[1])
        print(intrinsics_d, extrinsics_d, intrinsics_c, extrinsics_c)

        return intrinsics_d, extrinsics_d, intrinsics_c, extrinsics_c

    # Start the Color Camera
    def start_camera(self):
        if self.mock:
            return True
        # Start streaming
        try:
            self.profile = self.pipeline.start(self.config)
            print('\x1b[7;37;41m' + "Camera Connected" + '\x1b[0m')
        except Exception as e:
            print('\x1b[0;33;40m' + str(e) + '\x1b[0m')
            print('\x1b[1;37;43m' + "Wait for 2 seconds and try connect again ..." + '\x1b[0m')
            if e != KeyboardInterrupt:
                time.sleep(2)
                self.start_camera()

    # Stop the Depth Camera
    def stop(self):
        if self.mock:
            return True
        self.pipeline.stop()

    # Initialize color and depth camera (default 640 * 360 * 30fps)
    def create_streams(self):
        if self.mock:
            return True
        self.config.enable_stream(rs.stream.color, self.x, self.y, rs.format.bgr8, self.fps)
        self.config.enable_stream(rs.stream.depth, self.x, self.y, rs.format.z16, self.fps)

    # Enable the depth and color sync
    def sync(self):
        if self.mock:
            return True
        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

    # Return two frames from rgb and depth (aligned)
    def get_frame(self):
        self.frame_count += 1
        if self.mock:
            start = time.time()
            color = cv2.imread("/home/nvidia/pyCam/src/1.jpg")
            while time.time() - start < 1/30.0:
                pass
            return color, color, self.frame_count

        aligned_depth_frame = False
        color_frame = False
        while not aligned_depth_frame or not color_frame:
            # Get frameset of color and depth
            frames = self.pipeline.wait_for_frames()

            # Align the depth frame to color frames
            aligned_frames = self.align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

        # Return 3d Array
        color_image = np.asarray(color_frame.get_data())

        # Return 1D Array
        depth_image = np.asarray(aligned_depth_frame.get_data())
        # Convert the Depth image from uint16 to uint8
        depth_image = np.uint8(depth_image.astype(float) * 255 / 2 ** 12 - 1)
        # depth_image = 255 - cv2.cvtColor(depth_image, cv2.COLOR_GRAY2RGB)

        return color_image, depth_image, self.frame_count

    def get_compressed_frame(self):
        color, depth, id = self.get_frame()

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
        ret, jpeg = cv2.imencode('.jpg', color, encode_param)
        jpeg = jpeg.tobytes()
        depth = zlib.compress(depth)
        return jpeg, depth, id
