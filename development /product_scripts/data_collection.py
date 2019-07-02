from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import time
import imutils
from datetime import datetime
import pandas as pd
import os
import sys
sys.path.append('../utils')
import comm

#network client id
data_collector = None


currentThrottle = 0.0
currentSteering = 0.0


data_throttle=[]
data_steering=[]
data_images= []
dataSet = {'images':data_images,'steering ':data_steering,'throttle ':data_throttle}

timeStamp = "0.0.0.0"


#mqtt networking methods
def connected(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('RollE_MKII/steering_train')
    client.subscribe('RollE_MKII/throttle_train')

def message_in(client,userdata,msg):
    global currentSteering, currentThrottle, timeStamp
    timeStamp = datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f')
    
    if (msg.topic=='RollE_MKII/steering_train'):
        currentSteering = float(msg.payload)


    elif(msg.topic=='RollE_MKII/throttle_train'):
        currentThrottle = float(msg.payload)
        

def networking_init():

    #instantiates mqtt client connects to broker and awaits messages in endless loop
    global data_collector
    data_collector = comm.defineClient(client_id='data_collector')
    data_collector.on_connect = connected
    data_collector.on_message = message_in
    data_collector.connect(comm.BROKER)
    
    print('setting up done, starting ...')


def init():
    #initialize camera and grab reference to raw camera capture
    camera = PiCamera()
    camera.resolution =(200,66)
    camera.framerate=32
    rawCapture = PiRGBArray(camera, size=(200,66))# choose camera

    print("Warming up camera . . .")
    #allow camera warm up
    time.sleep(1)

    # initalize mqtt network
    networking_init()
    return camera,rawCapture

# compile dataset
def compile_data():
    df = pd.DataFrame(data=dataSet)
    #print(df.dtypes)

    print("Creating data csv file ...")
    # write to csv file without headers and index
    df.to_csv('data/driving_data.csv',index=False,header=False)
    time.sleep(1)
    print("File saved in data/driving_data.csv")


def start():
    #initialize run
    camera,rawCapture=init()

    try:
      while(True):
        # Capture frame-by-frame
        frame = next(camera.capture_continuous(rawCapture, format='bgr',use_video_port=True))
        frame = frame.array

        # cv2.imshow('frame',frame)
        data_collector.loop() #blocks code to check subscription for published values

        #resize image to reduce size
        #data_img=imutils.resize(frame, width=min(400, frame.shape[1]))
        data_img=frame
        
        img_name= "data/IMG/"+timeStamp+".png"
        
      # create storage folder if it doesnt already exist
        if not os.path.exists("data/IMG/"):
                os.makedirs("data/IMG/")
      #save processed image with time stamp
        cv2.imwrite(img_name,data_img)

        #clear stream in prep for next frame
        rawCapture.truncate(0)

        # write new data to dataset
        data_throttle.append(currentThrottle)
        data_steering.append(currentSteering)
        data_images.append(img_name)
        print("Img Name: {}, currentThrottle : {} , currentSteering : {}".format(img_name,currentThrottle,currentSteering))
      
        # if cv2.waitKey(100) & 0xFF == ord('q'):
        #     break

     # catch CTRL+C interrupt so data collecting loop can be broken and packaged into csv before quit   
    except KeyboardInterrupt:
             compile_data()
    # When everything done, release the capture


# only run if script if invoked directly
if __name__ == "__main__": 
    start()







