# Adding sources

Add sources (need to be done as root). From [here](https://askubuntu.com/questions/663837/unable-to-locate-package-libfaac-dev)

```bash
sudo -i
sudo echo "deb http://us.archive.ubuntu.com/ubuntu trusty main multiverse" >> /etc/apt/sources.list
exit
```

Add keys

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
```
# Install packages
From [here](https://gist.github.com/raulqf/f42c718a658cddc16f9df07ecc627be7)

First of all install update and upgrade your system:
```bash
sudo apt update
sudo apt upgrade
```

Then, install required libraries:

* Generic tools
```bash
sudo apt install build-essential cmake pkg-config unzip yasm git checkinstall
```

* Image I/O libs
```bash
sudo apt install libjpeg-dev libpng-dev libtiff-dev
```

* Video/Audio Libs - FFMPEG, GSTREAMER, x264 and so on.
```bash
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libavresample-dev
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt install libxvidcore-dev x264 libx264-dev libfaac-dev libmp3lame-dev libtheora-dev 
sudo apt install libfaac-dev libmp3lame-dev libvorbis-dev
```

* OpenCore - Adaptive Multi Rate Narrow Band (AMRNB) and Wide Band (AMRWB) speech codec
```bash
sudo apt install libopencore-amrnb-dev libopencore-amrwb-dev
```

* Cameras programming interface libs
```bash
sudo apt-get install libdc1394-22 libdc1394-22-dev libxine2-dev libv4l-dev v4l-utils
cd /usr/include/linux
sudo ln -s -f ../libv4l1-videodev.h videodev.h
cd ~
```

* GTK lib for the graphical user functionalites coming from OpenCV highghui module
```bash
sudo apt-get install libgtk-3-dev
```

* Python libraries for python3
```bash
sudo apt-get install python3-dev python3-pip
sudo -H pip3 install -U pip numpy
sudo apt install python3-testresources
```

* Parallelism library C++ for CPU
```bash
sudo apt-get install libtbb-dev
```

* Optimization libraries for OpenCV
```bash
sudo apt-get install libatlas-base-dev gfortran
```

* Optional libraries
```bash
sudo apt-get install libprotobuf-dev protobuf-compiler
sudo apt-get install libgoogle-glog-dev libgflags-dev
sudo apt-get install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen
```

# Download CV2 from source

Download

```bash
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.2.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.2.zip
```

Unzip and create build directory
```bash
unzip opencv.zip
unzip opencv_contrib.zip
mkdir build
```

# Compile CV2
Modified from [here](https://gist.github.com/raulqf/f42c718a658cddc16f9df07ecc627be7)

```bash
cd build

sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
-DBUILD_opencv_python3=yes \
-DHAVE_opencv_python3=ON \
-D CMAKE_C_COMPILER=/usr/bin/gcc-8 \
-DPYTHON3_EXECUTABLE=/opt/conda/bin/python3.7 \
-DPYTHON3_LIBRARY=/opt/conda/lib/libpython3.7m.so \
-DOPENCV_PYTHON3_INSTALL_PATH=/opt/conda/lib/python3.7/site-packages \
-DPYTHON3_INCLUDE_DIR=/opt/conda/include \
-DPYTHON3_PACKAGES_PATH= /opt/conda/lib/site-packages \
-DPYTHON3_NUMPY_INCLUDE_DIR= /opt/conda/lib/python3.7/site-packages/numpy/core/include \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.5.2/modules \
-DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-DBUILD_SHARED_LIBS=OFF \
-DBUILD_TESTS=OFF \
-DBUILD_PERF_TESTS=OFF \
-DBUILD_EXAMPLES=OFF \
-DWITH_OPENEXR=OFF \
-DWITH_CUDA=ON \
-DWITH_CUBLAS=ON \
~/opencv-4.5.2
```

# Fixing python Installation
Copying missing files to the correct directory. From [here](https://github.com/opencv/opencv/issues/6464#issuecomment-213950561)

```bash
cd /opt/conda/include/python3.7m/
sudo cp -a . ..
```

# Install CV2

```bash
cd ~/build
sudo make -j8 install
```

# Solving import CV2 problems
Do both solutions. From [here](https://stackoverflow.com/questions/50177330/how-to-deal-with-importerror-usr-lib-x86-64-linux-gnu-libatk-1-0-so-0-undefi
)

* Solution 1: Install glib as root
```bash
sudo -i
conda install -c anaconda glib
exit
```

* Solution 2: Changing file names
```bash
cd /opt/conda/lib
sudo mv libglib-2.0.so.0 libglib-2.0.so.0.backup
sudo mv libgstaudio-1.0.so.0 libgstaudio-1.0.so.0.backup
```


# My history (just in case)

```bash
cd ~
cd build
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE         -DBUILD_opencv_python3=yes         -DHAVE_opencv_python3=ON         
-D CMAKE_C_COMPILER=/usr/bin/gcc-8         -DPYTHON3_EXECUTABLE=/opt/conda/bin/python3.7         -DPYTHON3_LIBRARY=
/opt/conda/lib/libpython3.7m.so         -DOPENCV_PYTHON3_INSTALL_PATH=/opt/conda/lib/python3.7/site-packages       
  -DPYTHON3_INCLUDE_DIR=/opt/conda/include         -DPYTHON3_PACKAGES_PATH= /opt/conda/lib/site-packages         -D
PYTHON3_NUMPY_INCLUDE_DIR= /opt/conda/lib/python3.7/site-packages/numpy/core/include         -D OPENCV_EXTRA_MODULE
S_PATH=~/opencv_contrib-4.5.2/modules         -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda         -D CMAKE_INSTALL_PREF
IX=/usr/local        -DBUILD_SHARED_LIBS=OFF        -DBUILD_TESTS=OFF        -DBUILD_PERF_TESTS=OFF        -DBUILD_
EXAMPLES=OFF        -DWITH_OPENEXR=OFF        -DWITH_CUDA=ON        -DWITH_CUBLAS=ON         ~/opencv-4.5.2
nproc
make -j4 install
make -j\4 install
make -j8 install
sudo make -j8 install
cd src
cd /
ls
cd src
cd opt
ls
cd conda
ls
cd lib
ls
ls libgllib*
sudo -i
sudo mv libglib-2.0.so.0 libglib-2.0.so.0.backup
ls
sudo mv libgstaudio-1.0.so.0 libgstaudio-1.0.so.0.backup
sudo nano /etc/apt/sources.list
cd /opt/conda/include/python3.7m/
ls
cd ..
ls
sudo -i
cd /opt
cd conda
ls
cd lib
ls
cat libglib-2.0.so.0.backup
```