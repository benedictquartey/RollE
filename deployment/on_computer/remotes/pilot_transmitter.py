from time import sleep
import serial
import sys
sys.path.append('../utils')
import comm

#network client id
pilot = None


def networking_init():
    #instantiates mqtt client connects to broker and awaits messages in endless loop
    global pilot
    pilot = comm.defineClient(client_id='pilot')
    comm.publisher_init(client=pilot)

def send_value(val,topic):
    val = float(val)
    comm.publish_value(pilot,val,topic)

def send_stop_values():
    send_value(0000,'throttle_train')#send to training topic
    send_value(0000,'steering_train') 

    send_value(0000,'steering') #send to driving topic
    send_value(0000,'throttle')#send to driving topics
# start of program

def main():
    SerialPort= "/dev/cu.usbmodem"+sys.argv[1]
    ser = serial.Serial(SerialPort, 9600) # Establish the connection on a specific port, 9600 is baud rate of serial connection
    networking_init()

    try:
        while True:
            # ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
            result = str(ser.readline())
            # print(result)

            if("b'Throttle" in result):
                # remove identifying header
                throttle=(result[11:])
                # find index of end symbol
                delStart = throttle.find(':')
                # select only float value removing \r\n
                throttle_val = float(throttle[:delStart])

        # send via mqtt
                send_value(throttle_val,'throttle')#send to driving topic
                send_value(throttle_val,'throttle_train')#send to training topic

            if("b'Steering" in result):
                # remove identifying header
                steering=(result[11:])
                # find index of end symbol
                delStart = steering.find(':')
                # select only float value removing \r\n
                steering_val = float(steering[:delStart])

        # send via mqtt
                send_value(steering_val,'steering') #send to driving topic
                send_value(steering_val,'steering_train') #send to training topic

            if("b'Control" in result):
                delStart = steering.find(':')
                cmd = result[:delStart]
                send_stop_values()
                print("Closing Transmitter...")
                break

    except KeyboardInterrupt:
        pass
        send_stop_values()

            # print (throttle) # Read the newest output from the Arduino


# only run if script if invoked directly
if __name__ == "__main__": 
    main()
