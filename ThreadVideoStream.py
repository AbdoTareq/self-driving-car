# import the necessary packages
from imutils.video.webcamvideostream import WebcamVideoStream
from threading import Thread

class ThreadVideoStream:
    def __init__(self, resolution=(320,240), framerate=32):
        
        from imutils.video.pivideostream import PiVideoStream
        # initialize the picamera stream and allow the camera
        # sensor to warmup
        self.stream = PiVideoStream(resolution=resolution,
            framerate=framerate)

    def start(self):
        # start the threaded video stream
        #self.stream.start()
        #Thread(target=self.update, args=()).start()
        return Thread(target=self.update, args=()).start()
        #return self.stream.start()

    def update(self):
        # grab the next frame from the stream
        self.stream.update()

    def read(self):
        # return the current frame
        return self.stream.read()

    def stop(self):
        # stop the thread and release any resources
        self.stream.stop()
