#!/usr/bin/env python

# Usage:
# 1. Install Python dependencies: cv2, flask.
# 2. Run "python main.py".
from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

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
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='173.250.247.126', port='5000', debug=True)
