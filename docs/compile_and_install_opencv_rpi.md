# How to compile and install openCV on your raspberry pi

## Expand Filesystem 

1. Start raspi config

```bash 
	sudo raspi-config
```

2. navigate to 
	-> Advanced Options
	and choose 
	-> A1 expand Filesystem

3. restart RBP

```bash
	sudo shutdown -r now
```


## Install dependencies

```bash
	sudo apt-get update
	sudo apt-get upgrade
```

reboot again

```bash
	sudo shutdown -r now
```

after the reboot install cmake

```bash
	sudo apt-get install build-essential cmake pkg-config -y
```

install Image i/o


```bash
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
```

instal video i/o packages

```bash
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt-get install libxvidcore-dev libx264-dev -y
```

install the GTK dev lib for basics GUI Windows
```bash
sudo apt-get install libgtk2.0-dev libgtk-3-dev -y
```

## Install Python3, setuptools, dev and numpy

```bash
sudo apt-get install python3 python3-setuptools python3-dev -y
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install numpy
```

## Download openCV

```bash
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip
unzip opencv_contrib.zip
```

## compile and install openCV

```bash
cd opencv-3.4.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D BUILD_opencv_java=OFF \
-D BUILD_opencv_python2=OFF \
-D BUILD_opencv_python3=ON \
-D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D BUILD_EXAMPLES=ON\
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
-D WITH_CUDA=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS= OFF ..
```

## change swap size


```bash
sudo nano /etc/dphys-swapfile
```

### find the passage below and change to 1025 and comment out the 100
 
>#set size to absolute value, leaving empty (default) then uses computed value  
>#you most likely don't want this, unless you have an special disk situation  
>#CONF_SWAPSIZE=100  
>CONF_SWAPSIZE=1024  

### restart the swap process

```bash
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

## setup up the count of the cores on which the rpi should compile

```bash
make -j4
```

## install the build on RBP

```bash
sudo make install
sudo ldconfig
```

## verify if anything is installed correctly

```bash
ls -l /usr/local/lib/python3.5/dist-packages/
```

Look for a name like cv2.so and if it is not there then look for a name like cv2.cpython-35m-arm-linux-gnueabihf.so  
(name starting with cv2. and ending with .so). It might happen due to some bugs in Python binding library for Python 3.

We need to rename cv2.cpython-35m-arm-linux-gnueabihf.so to cv2.so using the following command:

```bash
cd /usr/local/lib/python3.5/dist-packages/
sudo mv /usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

```

## Test the build

```bash
python3 
```

```python
import cv2
cv2.__version__
```

## clean up the zip

```bash
cd ~
rm opencv.zip opencv_contrib.zip
```

## change swap size back


```bash
sudo nano /etc/dphys-swapfile
```

### find the passage below and change to 1025 and comment out the 100
 
>#set size to absolute value, leaving empty (default) then uses computed value  
>#you most likely don't want this, unless you have an special disk situation  
> CONF_SWAPSIZE=100  
>#CONF_SWAPSIZE=1024  

### restart the swap process

```bash
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

