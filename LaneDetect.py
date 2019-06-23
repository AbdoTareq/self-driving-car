import cv2
import numpy as np
# 'as' to make alias to use short word like plt => matplotlib.pyplot
import matplotlib.pyplot as plt
import time
from threading import Thread
from math import sqrt

        
def getLane(frame):
    return Thread(target=update, args=(frame)).start()
   
def start(frame):
#    canny_image = canny(frame)
    #cv2.imshow("masked", canny_image)
    masked_image = mask_image(frame)
    cropped_image = region_of_interest(masked_image)
    cv2.imshow("masked", cropped_image)
    canny_image = canny(cropped_image)
    lines = cv2.HoughLinesP(canny_image, 1, np.pi / 180, 30, np.array([]), minLineLength=5, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    image_line_detected = cv2.addWeighted(frame, .8, line_image, 1, 1)
    cv2.imshow("lines", image_line_detected)
    return averaged_lines, image_line_detected

#this function detects regions of gradient colors (colors change regions)
def canny(image):
    # converts an image to gray
#    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # reduce image noise on gray 5x5 scale and it's useless here as it's canny fun already has a built in GaussianBlur
    blur = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    # it detects sharp edges which are the lines between every 2 diffrent color regions and 1 : 3 (50:150) is
    # suitable for edges detection
    canny = cv2.Canny(blur, 125, 225)
    return canny

def mask_image(image):
            
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([180, 150,30], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(image, lower_black, upper_black)
    # Bitwise-AND mask and original im
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    
    return mask
    

# this fun is to color the wanted area of an image
def region_of_interest(image):
    # image height is the rows number
    height = image.shape[0]
    width = image.shape[1]
    # single polygon array as fillPoly() fills area bounded by polygon array
    polygons = np.array([[(int(width/4), int(height/3)), (int((3*width)/4), int(height/3))
                          , (width, int((2*height)/3)), (width, height)
                          , (0, height), (0, int((2*height)/3))]])
    # copy the same image but in black
    mask = np.zeros_like(image)
    # fillPoly() takes the image and polygons drawn on it and color of polygons white 255
    # and draw the polygon on the image
    cv2.fillPoly(mask, polygons, 255)
    # we takes the image mask it with the region we want to keep the important region only
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# draw lines on image
def display_lines(image, lines):
    # black image
    line_image = np.zeros_like(image)
    try:
        if lines is not None:
            for x1, y1, x2, y2 in lines:
                # draw a line on image
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0,), 5)
        return line_image
    except :
        print('exception2')
        return line_image

# this fun to group near lines into single one
def average_slope_intercept(image, lines):
    # left lines in the line images
    left_fit = []
    left_max_distance = 0 
    # right lines in the line images
    right_fit = []
    right_max_distance = 0 
    if lines is not None:
        for line in lines:
            # convert 2d array to 1d array of 2 points
            x1, y1, x2, y2 = line.reshape(4)
            # gives us line slope & y intercept
            line_parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = line_parameters[0]
            y_intercept = line_parameters[1]
            distance = sqrt((x1-x2)**2 + (y1-y2)**2)
            if slope < 0:
                if(distance > left_max_distance):
                    left_fit = (slope, y_intercept)
                    left_max_distance = distance
#                    print('left distance : ')
#                    print(distance)
            else:
                if(distance > right_max_distance):
                    right_fit = (slope, y_intercept)
                    right_max_distance = distance
        if( left_max_distance != 0 and right_max_distance != 0 ):
            left_line = make_cordinates(image, left_fit)
            right_line = make_cordinates(image, right_fit)            
#            left_slope = (left_line[3] - left_line [1]) / (left_line[2] - left_line[0])
#            right_slope = (right_line[3] - right_line [1]) / (right_line[2] - right_line[0])
            return np.array([left_line, right_line])
        elif left_max_distance != 0:
            left_line = make_cordinates(image, left_fit)
            return np.array([left_line, [0,0,0,0]])
        elif right_max_distance != 0:
            right_line = make_cordinates(image, right_fit)
            return np.array([[0,0,0,0], right_line])
    else :
        return np.array([[0,0,0,0], [0,0,0,0]])


def make_cordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
        if slope != 0:
            y1 = image.shape[0]
#            y2 = int(y1 * 3 / 5)
            y2 = 0
            x1 = int((y1 - intercept) / slope)
            x2 = int((y2 - intercept) / slope)
            return np.array([x1, y1, x2, y2])
    except:
        print('exception')
    