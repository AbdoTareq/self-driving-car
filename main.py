import time
import numpy as np
import cv2
import math

from ThreadVideoStream import ThreadVideoStream
from MoveCarPWM import MoveCar
from UltraSensor import UltraSensor
from LaneDetect import *
from sign_rec import *
from math import inf

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

class PID_CONTROLLER:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.p_error = 0
        self.i_error = 0
        self.d_error = 0
        
    def update_error(self, cte):
        self.d_error = cte - self.p_error
        self.p_error = cte
        self.i_error += cte
        
    def total_error(self):
        return (-self.kp * self.p_error) - (self.ki * self.i_error) - (self.kd * self.d_error)

def get_slope(line):
    x_diff = line[0] - line[2]
    y_diff = line[1] - line[3]
    if x_diff != 0:
        return y_diff / x_diff
    else :
        return math.inf

if __name__ == '__main__':
    
    #initialize camera
    cap = ThreadVideoStream(resolution=(320, 240), framerate=32)
    cap.start()
    time.sleep(1.0)
    
    pid = PID_CONTROLLER(0.05, 0.0001, 1.5)
    
    #create car object
    car = MoveCar()
    car.initialize()
    
    #initialize ultrasonice sensor
    usensor = UltraSensor()
    
    while True:
        
        try :
            
			#get the current frame
            frame = cap.read()
            
			#get the lines and the processed image
            lines, image_lines = start(frame)
            
            #get ultrasonice sensro measured distance
            dist = usensor.distance()
                            
            #get the signs direction
            direction, sign_image = findTrafficSign(frame)
            
			#show the final image
            cv2.imshow('signs', sign_image)
                         
			#get the left and right lines
            left_line = lines[0]
            right_line = lines[1]
            
            if cv2.waitKey(1) == ord('q'):
                break
            
			#if turn back sign found stop car
            if direction == 'Turn Back' :
                car.stop_car()
                continue
			#if turn right sign found turn car right
            elif direction == 'Turn Right' :
                car.move_right()
                continue
			#if turn left sign found turn car left
            elif direction == 'Turn Left' :
                car.move_left()
                continue
			#if measured distance is less than 40 meters stop car
            elif dist < 40 :
                car.stop_car()
                continue
			#if move straight sign found move car straight
            elif direction == 'Move Straight' :
                car.move_forward()
                continue
            
			#else if both lines found
            if not np.array_equal(left_line, [0, 0, 0, 0]) and  not np.array_equal(right_line, [0, 0, 0, 0]) :
                
				#calculate center error(cte)
                center_x, center_y = line_intersection([[left_line[0], left_line[1]], [left_line[2], left_line[3]]]
                                        , [[right_line[0], right_line[1]], [right_line[2], right_line[3]]])
                cte = 160 - center_x
                
				#adjust the steering angle according to the cte
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
                #if no lines detected keep moveing forward
                car.move_forward()
            elif np.array_equal(left_line, [0, 0, 0, 0]) :
                #if only right line found move right
                x1 = right_line[0]
                y1 = right_line[1]
                x2 = right_line[2]
                y2 = right_line[3]
				
				#calculate slope
                theta = math.atan((y2-y1)/(x2-x1))
				
				#move the car with an angle according to the slope
                car.move_with_angle(abs(theta-0.7)*100, 100)
            else :
                #if only left line found move left
                x1 = left_line[0]
                y1 = left_line[1]
                x2 = left_line[2]
                y2 = left_line[3]
				
				#calculate slope
                theta = math.atan((y2-y1)/(x2-x1))
				
				#move the car with an angle according to the slope
                car.move_with_angle(100, abs(theta+0.7)*100)
                
            
        except Exception as e:
            print('Exception: '+ str(e))
