# drOneS 

drOneS is a python project to control a drone with a remote controller. 
This Project is ment to be run on a raspberry pi. Using GPIO pins and a NRF24
radio module.

----

### What does this program

this program creates an multithreaded process. The program needs to listen on the drones input and on the remote
controls input. To avoid a blocking state these things are running in different threads.
The threads can interact with each other

#### Websocket Thread

the websocket provides data about height, speed, accelration, gps-data, etc to all 
connected LUNA application (pc, anroid). The Websocket accepts also commands from the app as
engine start, engine off, etc. 

#### flask Webserver thread

The flask Webserver works as a proxy and send the video from the drone to all connected 
devices via udp. 

#### arduino_bridge thread

the arduino bride sends and receive all radio informations from the drone and put them to the websocket queue. 
The Websocket que process all these data and send it further to the apps. 

#### the hardware thread

The hardware thread controls the gpio pins of the pi and gets data about battery status, led etc.

## installation

1. clone repository *git clone http://gitlab.kuckelsberg.eu/drones/threadding_airc.git
2. install dependencies *pip3 install -r requirements.txt*

## run 

1. *python3 airc_os.py*

## usage

this projects needs to be run when raspbian is bootet completly.
