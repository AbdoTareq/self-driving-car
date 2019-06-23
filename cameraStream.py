# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from PIL import Image
from threading import Condition
from http import server
import numpy as np
import cv2
import math

from MoveCarPWM import MoveCar
from UltraSensor import UltraSensor
from LaneDetect import *
from sign_rec import *
from math import inf


PAGE="""\
<html>
<head>
<title>Autonomous Car Project</title>
</head>
<body>
<center><h1>Autonomous Car Project</h1></center>
<center><img src="stream.mjpg" width="480" height="360"></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                
                #create car object
                car = MoveCar()
                car.initialize()
    
                #initialize ultrasonice sensor
                usensor = UltraSensor()
                        
                while True:
                    with output.condition:
                        output.condition.wait()
                        
                        #get the current frame
                        frame = output.frame
                        
                        try :
                            
                            #convert it into numpy array
                            imagee = cv2.imdecode(np.fromstring(frame, dtype = np.uint8), 1)
                            
                            #do the image proccess on it and store the value into line_image variable
                            lines, image_lines = start(imagee)
                            
                            left_line = lines[0]
                            right_line = lines[1]
                            
                            #get ultrasonice sensro measured distance
                            dist = usensor.distance()
                            
                            #get the signs direction
                            direction, sign_image = findTrafficSign(image_lines)
                            
                            if direction == 'Turn Back' :
                                car.stop_car()
                            elif direction == 'Turn Right' :
                                car.move_right()
                            elif direction == 'Turn Left' :
                                car.move_left()
                            elif direction == 'Move Straight' :
                                car.move_forward()
                            elif dist < 40 :
                                car.stop_car()
                            else :
                                                    
                                if not np.array_equal(left_line, [0, 0, 0, 0]) and  not np.array_equal(right_line, [0, 0, 0, 0]) :
                                    
                                    print('both')
                                    center_x, center_y = line_intersection([[left_line[0], left_line[1]], [left_line[2], left_line[3]]]
                                                            , [[right_line[0], right_line[1]], [right_line[2], right_line[3]]])
                                    cte = center_x - 160
                                    
                                    print(cte)
                                    
                                    if cte < 10 and cte > -10 :
                                        car.move_forward()
                                    elif cte > -80 and cte < -10:
                                        car.move_with_angle(75, 100)
                                    elif cte < -80:
                                        car.move_with_angle(50, 100)
                                    elif cte > 10 and cte < 80:
                                        car.move_with_angle(100, 75)
                                    elif cte > 80:
                                        car.move_with_angle(100, 50)
                                    else :
                                        car.move_forward()
                                    
                                elif np.array_equal(left_line, [0, 0, 0, 0]) and np.array_equal(right_line, [0, 0, 0, 0]):
                                    #no lines detected
                                    print('no lines')
                                    car.move_forward()
                                elif np.array_equal(left_line, [0, 0, 0, 0]) :
                                    #no left lines detected
                                    print('right slope')
                                    x1 = right_line[0]
                                    y1 = right_line[1]
                                    x2 = right_line[2]
                                    y2 = right_line[3]
                                    theta = math.atan((y2-y1)/(x2-x1))
                                    print(theta)
                                    car.move_with_angle(abs(theta-0.5)*100, 100)
                                else :
                                    #no right lines detected
                                    print('left slope')
                                    x1 = left_line[0]
                                    y1 = left_line[1]
                                    x2 = left_line[2]
                                    y2 = left_line[3]
                                    theta = math.atan((y2-y1)/(x2-x1))
                                    print(theta)
                                    car.move_with_angle(100, abs(theta+0.5)*100)
                                
                            #show image
                            final_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2RGB)
                            cv2.imshow('Image2', final_image)
                            key = cv2.waitKey(1)
                            
                            #convert the numpy array into PIL image
                            pil_image = Image.fromarray(final_image)
                            
                            #convert PIL image back to jpeg frame
                            imgByteArr = io.BytesIO()
                            pil_image.save(imgByteArr, format='JPEG')
                            frame = imgByteArr.getvalue()
                            
                        except Exception as e:
                            logging.warning(
                                'Found Error %s: %s',
                                self.client_address, str(e))
                        
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# change reslotion here will effect camera performance 500x240 lags 1s which is acceptable
with picamera.PiCamera(resolution='320x240', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

