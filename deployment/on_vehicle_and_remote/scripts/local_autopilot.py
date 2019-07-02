import numpy as np #matrix 
from keras.models import load_model
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

import cv2
import imutils
import sys
sys.path.append('../utils')
import comm

imageHeight, imageWidth, imageChannels = 66,200,3
 
#network client id
ai_pilot = None

#throttle power
throttle = 0.7


def init():
    global model
    print("loading model ... ")
    model = load_model(sys.argv[1])
    networking_init()

def predict(image):
    steering_angle = float(model.predict(image, batch_size=1)) #follow up check if model being called is the correct scope, because it is not declared anywhere globally
    return steering_angle
    

def networking_init():
    global ai_pilot
    ai_pilot = comm.defineClient(client_id='ai_pilot')
    comm.publisher_init(client=ai_pilot)


def send_value(val,topic):
    val = float(val)
    comm.publish_value(ai_pilot,val,topic)
    
 
def main():
  init()
  #initialize camera and grab reference to raw camera capture
  camera = PiCamera()
  camera.resolution =(200,66)
  camera.framerate=32
  rawCapture = PiRGBArray(camera, size=(200,66))# choose camera

  print("Warming up camera . . .")

  #allow camera warm up
  time.sleep(1)


  try:
    while(True):
      frame = next(camera.capture_continuous(rawCapture, format='bgr',use_video_port=True))
      frame = frame.array

      #resize image to reduce size
      #data_img=imutils.resize(frame, width=min(400, frame.shape[1]))
      img=frame
      img = img[38:,:,:] #crop to remove upwanted parts
      img = cv2.resize(img,(imageWidth, imageHeight),cv2.INTER_AREA)
      img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
      image = np.array([img])  
      steer_angle = predict(image)
      print(steer_angle)
      print("Steering Angle: ",steer_angle)
      send_value(throttle,'throttle')#send to driving topic
      send_value(steer_angle,'steering') #send to driving topic
      
      #clear stream for next image
      rawCapture.truncate(0)

  except KeyboardInterrupt:
          pass
          send_value(0000,'throttle_train')#send to training topic
          send_value(0000,'steering_train') 
          send_value(0000,'steering') #send to driving topic
          send_value(0000,'throttle')#send to driving topic



# only run if script if invoked directly
if __name__ == "__main__": 
    main()
