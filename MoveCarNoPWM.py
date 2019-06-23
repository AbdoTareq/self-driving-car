import RPi.GPIO as GPIO
import time

class MoveCar():
    def __init__(self):
        self.control=''
        #right wheels
        self.right_enable = 33
        self.right_input_1 = 13
        self.right_input_2 = 11
        #left wheels
        self.left_enable = 32
        self.left_input_1 = 16
        self.left_input_2 = 18
        
    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        #right wheels
        GPIO.setup(self.right_enable, GPIO.OUT)
        GPIO.setup(self.right_input_1, GPIO.OUT)
        GPIO.setup(self.right_input_2, GPIO.OUT)
        #left wheels
        GPIO.setup(self.left_enable, GPIO.OUT)
        GPIO.setup(self.left_input_1, GPIO.OUT)
        GPIO.setup(self.left_input_2 ,GPIO.OUT)
        
#        self.p1 = GPIO.PWM(self.right_enable, 20)    # Created a PWM object
#        self.p2 = GPIO.PWM(self.left_enable, 20)
#        self.p1.start(0)
#        self.p2.start(0)
        
    def move_forward(self):
        self.control='f'
        #right wheels
        GPIO.output(self.right_enable , GPIO.HIGH)
        #self.p1.ChangeDutyCycle(100)
        GPIO.output(self.right_input_1 , GPIO.LOW)
        GPIO.output(self.right_input_2 , GPIO.HIGH)
        #left wheels
        GPIO.output(self.left_enable , GPIO.HIGH) 
        #self.p2.ChangeDutyCycle(100)
        GPIO.output(self.left_input_1 , GPIO.LOW)
        GPIO.output(self.left_input_2 , GPIO.HIGH)
        
    def move_backward(self):
        self.control='b'
        #right wheels
        GPIO.output(self.right_enable , GPIO.HIGH)
        #self.p1.ChangeDutyCycle(100)
        GPIO.output(self.right_input_1 , GPIO.HIGH)
        GPIO.output(self.right_input_2 , GPIO.LOW)
        #left wheels
        GPIO.output(self.left_enable , GPIO.HIGH) 
        #self.p2.ChangeDutyCycle(100)
        GPIO.output(self.left_input_1 , GPIO.HIGH)
        GPIO.output(self.left_input_2 , GPIO.LOW)
        
    def move_left(self):
        #right wheels
        GPIO.output(self.right_enable , GPIO.HIGH)
        #self.p1.ChangeDutyCycle(100)
        GPIO.output(self.right_input_1 , GPIO.LOW)
        GPIO.output(self.right_input_2 , GPIO.HIGH)
        #left wheels
        GPIO.output(self.left_enable , GPIO.LOW) 
        #self.p2.ChangeDutyCycle(15)
        GPIO.output(self.left_input_1 , GPIO.LOW)
        GPIO.output(self.left_input_2 , GPIO.HIGH)
        
    def move_right(self):
        #right wheels
        GPIO.output(self.right_enable , GPIO.LOW)
        #self.p1.ChangeDutyCycle(15)
        GPIO.output(self.right_input_1 , GPIO.LOW)
        GPIO.output(self.right_input_2 , GPIO.HIGH)
        #left wheels
        GPIO.output(self.left_enable , GPIO.HIGH) 
        #self.p2.ChangeDutyCycle(100)
        GPIO.output(self.left_input_1 , GPIO.LOW)
        GPIO.output(self.left_input_2 , GPIO.HIGH)
        
    def stop_car(self):
        self.control=''
        #right wheels
        #GPIO.output(self.right_enable , GPIO.LOW)
        self.p1.ChangeDutyCycle(0)
        GPIO.output(self.right_input_1 , GPIO.LOW)
        GPIO.output(self.right_input_2 , GPIO.LOW)
        #left wheels
        #GPIO.output(self.left_enable , GPIO.LOW) 
        self.p2.ChangeDutyCycle(0)
        GPIO.output(self.left_input_1 , GPIO.LOW)
        GPIO.output(self.left_input_2 , GPIO.LOW)
        
    def brake(self):
        if(self.control==''):
            pass
        elif(self.control=='f'):
            print( "Applying brake.")
            self.move_backward()
            time.sleep(self.runtime)
            self.stop_car()
            self.control=''
        elif(self.control=='b'):
            print ("Applying brake.")
            self.move_forward()
            time.sleep(self.runtime)
            self.stop_car()
            self.control=''
        else:
            pass
        
    def close(self):
        GPIO.cleanup()
        
      
if __name__ == '__main__': 
    time.sleep(2)
    car = MoveCar()
    car.initialize()
    car.move_forward()
    time.sleep(2)
    car.move_backward()
    time.sleep(3)
    car.move_right()
    time.sleep(3)
    car.move_left()
    time.sleep(3)
    #car.brake()
    car.stop_car()
    car.close()
            