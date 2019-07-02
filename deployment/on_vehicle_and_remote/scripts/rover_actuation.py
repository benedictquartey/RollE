import Adafruit_PCA9685
import time
from datetime import datetime

import sys
sys.path.append('../utils')
import comm

#network client id
drive_controller = None

steering_servo_channel = 0
throttle_servo_channel = 8

left_angle = -1
right_angle = 1

throttle_min = -1
throttle_max = 1

#pusle length || time pwm cycle cycle should run, equivalent to measure of turn of servo

#servo_min = 150  # Min pulse length out of 4096 || turns towards left
#servo_max = 600  # Max pulse length out of 4096 || turns towards right

#choosing 290 and 490 instead of 150 and 600 reduces threshold turn sharpness limit of roll-2 mk II  
pulse_left = 290
pulse_right = 490

#throttle pulses determines threshold acceleration of roll-e || overall max value 300, overall min 490
throttle_pulse_max = 200
throttle_pulse_min = 390
throttle_pulse_zero = 350


#pwm frequency is 60 hz
frequency = 60
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(frequency)

def init():
    reset_steer()
    reset_throttle() #sending throttle_zero pulse calibrates electronic speed controller
    networking_init()


def range_map(x,X_min,X_max,Y_min,Y_max):
    #linear mapping betwwen two range of values
    
    X_range = X_max-X_min
    Y_range = Y_max-Y_min
    XY_ratio = X_range/Y_range
    y=((x-X_min) / XY_ratio + Y_min) // 1
    return int(y)

# #this method maps an angle to a pulse width, determingng how positing and timing of steering serveofor a turn
def steer(angle):
    #converts an angle value from -1 to 1 (including decimals) into PWM values, 0 being rest and -1 turns fully right

    steer_pulse = range_map(angle,
                            left_angle,
                            right_angle,
                            pulse_left,
                            pulse_right)
    
    pwm.set_pwm(steering_servo_channel,0,steer_pulse)
    #reset_steer()

    
def reset_steer():
    steer(0)
    print('steering reset')

def steer_raw(pulse_length):
    pwm.set_pwm(steering_servo_channel,0,pulse_length)

def throttle(accel_value):
    #converts accelerate values between -1 and 1 into PWM values, 0 being stop and -1 being forward.
    
    #reversing map
    if accel_value > 0:
        throttle_pulse = range_map(accel_value,
                                   0,
                                   throttle_max,
                                   throttle_pulse_zero,
                                   throttle_pulse_max
                                   )
    #accelerating forward map    
    else:
        throttle_pulse = range_map(accel_value,
                                   throttle_min,
                                   0,
                                   throttle_pulse_min,
                                   throttle_pulse_zero)
        
    pwm.set_pwm(throttle_servo_channel,0,throttle_pulse)
    

def reset_throttle():
    pwm.set_pwm(throttle_servo_channel,0,throttle_pulse_zero)
    time.sleep(1)
    

#mqtt networking methods

def connected(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #subscribe to base topic, thus receives from all sub topics
    client.subscribe('RollE_MKII/#')


def message_in(client,userdata,msg):
    print("Time: " + datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f') + "    Topic: "+msg.topic+"        Message: "+str(msg.payload))
  
    if (msg.topic=='RollE_MKII/steering'):
        angle = float(msg.payload)
        steer(angle)

    elif(msg.topic=='RollE_MKII/throttle'):
        accel = float(msg.payload)
        throttle(accel)
        

def networking_init():
    #instantiates mqtt client as subscriber connects to broker and awaits messages in endless loop
    global drive_controller
    drive_controller = comm.defineClient(client_id='drive_controller')
    drive_controller.on_connect = connected
    drive_controller.on_message = message_in
    drive_controller.connect(comm.BROKER)

    drive_controller.loop_forever()



def stop():
    pwm.set_pwm(throttle_servo_channel,0,throttle_pulse_zero)


# only run if script if invoked directly
if __name__ == "__main__": 
    init()





    
