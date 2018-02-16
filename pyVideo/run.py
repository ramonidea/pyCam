#!/usr/bin/env python
'''
Usage:
python run.py
Argument options:
-x {resolution X} -y {resolution Y} -fps {fps}
-rgb {t/f open/close rgb camera} -depth {t/f open/close depth camera}


'''

from sys import argv
from flask import Flask, render_template, Response
from camera import VideoCamera

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        rgb,depth = camera.get_frame()
        yield (b'--frame'+str.encode(str(len(rgb)))+b'f'+str.encode(str(len(depth)))+b'e\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + rgb + depth + b'\r\n\r\n')


@app.route('/video_feed')
def rgb_feed():
    return Response(gen(VideoCamera(x = videoX, y = videoY, fps = videoFps, rgb = rgb, depth = depth)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('camera_info')
def camera_info():
    return Response("-X"+str(videoX)+"-Y"+str(videoY)+"fps"+str(videoFps))


#Variables:
app = Flask(__name__)

videoX = 640
videoY = 480
videoFps = 30
rgb = True
depth = True

if __name__ == '__main__':

    myargs = getopts(argv)
    try:
        if "-x" in myargs:
            videoX = int(myargs["-x"])
        if "-y" in myargs:
            videoY = int(myargs["-y"])
        if "-fps" in myargs:
            videoFps = int(myargs["-fps"])
        if "-rgb" in myargs:
            rgb = True if myargs["-rgb"]=="t" else False
        if "-depth" in myargs:
            depth = True if myargs["-depth"]=="t" else False
    except Exception, e:
        print(e.message)
