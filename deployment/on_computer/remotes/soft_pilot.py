# allows for getting keybord input and  nice console app renedering
import curses
import time
# from development.utils import comm as comm

import sys
sys.path.append('../utils')
import comm


#network client id
soft_pilot = None


def init():
  global soft_pilot
  soft_pilot = comm.defineClient(client_id='soft_pilot')
  comm.publisher_init(client=soft_pilot)

def send_value(val,topic):
    val = float(val)
    comm.publish_value(soft_pilot,val,topic)

def main(win):
    init()
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Steering:           "+"Throttle:      ")
    steering_val=0
    throttle_val=0
    while 1:          
        try:               
           key = win.getkey()
           win.clear()      

# Throttle controlling           
           if key == 'w' and throttle_val>-1:
            # move forward
              throttle_val-=0.1

           if key == 's':
            # stop
                throttle_val=0

           if key == 'x' and throttle_val<1:
            # move backwards
              throttle_val+=0.1

# Steering controlling
           if key  == 'KEY_LEFT' and steering_val<1:
            # turn left
              steering_val+=0.2
           if key  == 'KEY_RIGHT' and steering_val>-1:
            # turn right
              steering_val-=0.2
           if key  == 'KEY_DOWN':
            # turn right
              steering_val=0

           win.addstr("Steering: "+str(steering_val)+"        ")
           win.addstr("Throttle: "+str(throttle_val))
           send_value(steering_val,'steering') #send to driving topic 
           send_value(steering_val,'steering_train') #send to training topic
           send_value(throttle_val,'throttle')
           send_value(throttle_val,'throttle_train')
      
        except Exception as e:
           # No input
           # win.addstr(str('0'))
           # val=0 
           pass     

try:
  curses.wrapper(main)

except KeyboardInterrupt:
  pass

send_value(0000,'throttle_train')#send to training topic
send_value(0000,'steering_train') 

send_value(0000,'steering') #send to driving topic
send_value(0000,'throttle')#send to driving topic


