
# RollE [Affordable Modular Autonomous Vehicle Development Platform]

Every year, 1.27 million people die in road accidents, 90% of which are down to human error. In 2015 there were 256,179 victims in Africa alone. RollE is an open-source programme to develop modular self-driving cars in a collaborative manner. Students and researchers have access to this technology to test their ideas and implement algorithms for autonomous driving, using learning and control techniques which are similar to those used in the automotive industry, but without having to take on the elevated relative costs.

* [Affordable Modular Autonomous Vehicle Development Platform](https://ieeexplore.ieee.org/document/8506757) - Paper on RollE published by IEEE
* [Data Collection and Autonomy Demonstration of RollE](https://www.youtube.com/watch?v=1iLejcGQvJw) - Video demonstration of RollE  


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.  See deployment for notes on how to deploy the project on a live system.

### Folder Structure
There are primarily two key folders of interest in this repo: [deployment](https://github.com/benedictquartey/RollE/tree/master/deployment) and [development](https://github.com/benedictquartey/RollE/tree/master/development).
Both these folders contain the same files, however they are structured differently.

The files in development are structured into the logical layers of the system to aide in working on code that contribute to a similar broader goal. 

```
	.
    ├── Development                   
    │   ├── learning            #machine learning and data
    │   │   ├── train.py 						
    │   │   ├── model.py
    │   │   ├── data_processing.py
    │   │   └── plots.py
    │   │       
    │   ├── control	            #interfaces with hardware components
    │   │   ├── rover_actuation.py 
    │   │   └── rollE_remote.ino
    │   │
    │   ├── product_scripts         #developed tools 
    │   │   ├── pilot_transmitter.py
    │   │   ├── soft_pilot.py
    │   │   ├── data_collection.py 
    │   │   └── local_autopilot.py
    │   │    
    │   └── utils                 #utilities  
    │       └── comm.py       
	└── ...
```

While the files in deployment are structured based on where they are run (either on the RollE vehicle and remote controller or the separate computer used for training and debugging)
```
	.
    ├── Deployment                   
    │   ├── on_computer            #code runs on computer
    │   │   ├── learning
    │   │   │   ├── train.py   
    │   │   │   ├── model.py    
    │   │   │   ├── data_processing.py
    │   │   │   └── plots.py
    │   │   │
    │   │   ├── remotes
    │   │   │   ├── pilot_transmitter.py   
    │   │   │   └── soft_pilot.py 
    │   │   │   
    │   │   └── utils 
    │   │       └── comm.py
    │   │      
    │   └── on_vehicle_and_remote           #code runs on vehicle (Raspberry Pi)
    │       ├── on_remote_controller     
    │       │   └── rollE_remote.ino
    │       │   
    │       ├── scripts
    │       │   ├── local_autopilot.py
    │       │   ├── rover_actuation.py   
    │       │   └── data_collection.py 
    │       │   
    │       └── utils 
    │           └── comm.py 
	└── ...
```

## Setting up environment on computer

A step by step series of instructions to setup an environment for RollE

* Install the Python 3 miniconda package manager for your OS from [here](https://docs.conda.io/en/latest/miniconda.html)

* Navigate to the misc folder and download the [rolle_env.yml](https://github.com/benedictquartey/RollE/tree/master/misc) file

* Open up a terminal or command prompt window on your computer, change directory into your downloads folder and run the command below to create a python environment called "rolle" with all necesarry dependencies installed. 

```
conda env create -f rolle_env.yml"
```

* You new environment can be activated by running the code below

```
conda activate rolle 
```

Find help with managing environments [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)




## Setting up environment on vehicle (Raspberry Pi)

Brace yourself, setting up a Raspberry Pi can be a little cumbersome, but trust me it is worth it. Lets go ...

* Install Raspbian Stretch and activate VNC on your Raspberry Pi
* Run the commands below in the command line

```
pi@raspberry:~ $ sudo apt-get update && sudo apt-get upgrade
pi@raspberry:~ $ sudo pip install --upgrade pip
```

* Run the command below to install [mosquitto](https://mosquitto.org/)
```
pi@raspberry:~ $ sudo apt-get install mosquitto mosquitto-clients 
```

* Follow this great [tutorial](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) to install OpenCV, PiCamera and set up a virtual environment on your Raspberry Pi. Be sure to look for the Raspberry Pi section as there are installation instructions for multiple platforms. Also ensure to follow "Option B: Install OpenCV into a virtual environment with pip on your Raspberry Pi"

When creating the virtual environment (with "mkvirtualenv cv -p python3.5") make sure to create a Python 3.5 environment


* While working in the virtual Python 3.5 environment created in the above step run the following commands to install more depencies into our working environment

```
pi@raspberry:~ $ pip install paho-mqtt
pi@raspberry:~ $ pip --no-cache-dir install pandas
pi@raspberry:~ $ pip install numpy
```

* Follow the "Configuring Pi For i2C" and "Hooking it Up" sections of this [tutorial](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-p) to setup your Raspberry Pi with the Adafruit pca9685 servo driver
```
pi@raspberry:~ $ sudo pip install adafruit-pca9685
```

* While still in our working Python3 virtual environment, Run the commands below to install keras version 2.1.5 and tensorflow version 1.0.1 (Found in the [misc](https://github.com/benedictquartey/RollE/tree/master/misc) folder)

```
pi@raspberry:~ $ pip install tensorflow-1.0.1-cp35-cp35m-linux_armv7l.whl       #pip install tensorflow from locally availiable wheel file 
pi@raspberry:~ $ sudo apt-get install libblas-dev liblapack-dev gfortran
pi@raspberry:~ $ sudo apt-get install python3-dev python3-setuptools
pi@raspberry:~ $ sudo apt-get install libhdf5-serial-dev
pi@raspberry:~ $ pip install h5py
pi@raspberry:~ $ pip install scipy --no-cache-dir
pi@raspberry:~ $ pip install pillow imutils
pi@raspberry:~ $ pip install keras==2.1.5
```

## Testing environment setup on Raspberry Pi
To test your environment open up a terminal, source the ~/.profile file, then activate the virtual environment you created while setting up the Pi
```
pi@raspberry:~ $ source ~/.profile
pi@raspberry:~ $ workon foo      #where foo is what you named the virtual environment
``` 
### Test python version
```
pi@raspberry:~ $ python --version

#desired output
Python 3.5.3
```
### Test Keras version
```
pi@raspberry:~ $ pip show keras

#desired output
Name: Keras
Version: 2.1.5
Summary: Deep Learning for humans
Home-page: https://github.com/keras-team/keras
Author: Francois Chollet
Author-email: francois.chollet@gmail.com
License: MIT
Location: /home/pi/.virtualenvs/rollepy3/lib/python3.5/site-packages
Requires: scipy, six, pyyaml, numpy
```
### Test tensorflow version
```
pi@raspberry:~ $ pip show tensorflow

#desired output
Name: tensorflow
Version: 1.0.1
Summary: TensorFlow helps the tensors flow
Home-page: http://tensorflow.org/
Author: Google Inc.
Author-email: opensource@google.com
License: Apache 2.0
Location: /home/pi/.virtualenvs/rollepy3/lib/python3.5/site-packages
Requires: six, numpy, wheel, protobuf
```

### Test opencv and other dependencies version
```
pi@raspberry:~ $ python
import cv2
import Adafruit_PCA9685
import pandas
```
All importations should be successfully executed


# Deployment
RollE can either be run in a "Data collection mode" or "Autonomous mode".
### Data collection mode: 
 In the data collection mode, RollE is controlled by a human agent using either the RollE Pilot (remote controller) or a console remote-control application [Soft Pilot](https://github.com/benedictquartey/RollE/tree/master/deployment/on_computer/remotes/soft_pilot.py). In this mode, image frames are captured from the camera. Each frame is stored with a timestamp and the corresponding throttle and steering values sent from the remote controller at the time of capture. At the end of a data collection run, the images are stored in a folder and the records of steering and throttle commands compiled and saved in a csv file. 
 
 The data from a data collection run is used to train an end-to-end convolutional neural network based on an architecture proposed by Nvidia and implemented using Keras, a neural network application programming interface.

 To start data collection mode, 
 * Log onto RollE's onboard Raspberry pi, you can use VNC to do this in headless mode. Make sure both your computer and raspberry pi are connected to RollE's onboard wireless network
 * Open up a terminal, source the ~/.profile file, then activate the virtual environment you created while setting up the Pi

* Run the [rover_actuation](https://github.com/benedictquartey/RollE/tree/master/deployment/on_vehicle_and_remote/scripts/rover_actuation.py) file
 ```
 pi@raspberry:~ $ python rover_actuation.py  #background process that handles control and would always be running in the background
 ```
* On your computer, open up a terminal, activate the virtual environment created when setting up the computer
```
conda activate rolle
```
* Run the [soft_pilot](https://github.com/benedictquartey/RollE/tree/master/deployment/on_computer/remotes/soft_pilot.py) (virtual remote controller) file.
```
python soft_pilot.py   
```
Keys
Left and right arrow keys on the keyboard will steer rolle, 
Down arrow key would set steering to default middle position
"w" accelerates and "x" decelerates 
"s"  brakes
* Run the [data_collection](https://github.com/benedictquartey/RollE/tree/master/deployment/on_vehicle_and_remote/scripts/data_collection.py) program. Once this is running you can start driving RollE around. 

Each of the running modules implement publish-subscribe based inter-process communication. When satisfied with the amount of data collected simply end the script with (Ctrl-C), steering and throttle values for your run will be collated and stored. This data can be used to train the convolutional neural network with the [train.py](https://github.com/benedictquartey/RollE/tree/master/deployment/on_computer/learning/train.py) script.



### Autonomous mode: 
In autonomous mode, RollE is controlled by an autopilot. The camera repeatedly captures frames of its environment and the autopilot software, running locally on RollE, uses the trained convolutional neural network model to predict steering angles for each frame. The throttle value for speed control is set to a constant value. 

To run RollE in autonomous mode,
* Run the [rover_actuation](https://github.com/benedictquartey/RollE/tree/master/deployment/on_vehicle_and_remote/scripts/rover_actuation.py) file
 ```
 pi@raspberry:~ $ python rover_actuation.py  #background process that handles control and would always be running in the background
 ```

* Make sure the *.h5 model file generated from training with [train.py](https://github.com/benedictquartey/RollE/tree/master/deployment/on_computer/learning/train.py) is in your working directory then run the local_autopilot.py (pass in the name of the model as an argument)
```
pi@raspberry:~ $ python3 rover_actuation.py modelName.h5
```


## Contributing

Contributions are welcome and enccouraged, create a pull request to submit contributions.


## Author

* **Benedict Quartey** 

Kindly acknowledge the creator when using all or any section of the code/design. If you have any inquiries or need any help, shoot me an email at benedict.quartey@ashesi.edu.gh

## License
This project is licensed under the MIT License. Refer to the LICENSE file for details



