# Self-driving-car(Fayoum University)


An autonomous car that can guide itself inside a lane, by processing the input image, detect the 
lane borders and take the decision.

# Car components 

  - Raspberry pi.
  - Camera module.
  - Ultrasonic sensor
  - Batteries for mottors.
  - Powerpank for raspberry.
  - L298 dual motor driver.

### Installed on raspberry

We uses a number of libraries to work properly:

* OpenCv
* Python 3
* numpy

### Test instructions

Run main.py to run the lane detection code and make the car drive inside the lanes.
Run cameraStream.py if you want to watch live stream from the camera while car is driving inside lanes you can see the stream at http://<Your_Pi_IP_Address>:8000.

**Test & presentation links**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   https://www.youtube.com/watch?v=753BEYi6eoo&t
   
   https://www.youtube.com/watch?v=753BEYi6eoo&t


MIT License

Copyright (c) 2019 Abdelrahman Tareq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
