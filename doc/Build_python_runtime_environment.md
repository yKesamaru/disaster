# Build python runtime environment
Here is an example of building a python3.7 runtime environment using `pyenv` and `venv`.  
Installing pyenv is not required, but it is recommended to avoid affecting your system python.  

## The following tools are used to build this environment
* Switch interpreter
  * pyenv
* Switch package
  * venv
* Install package
  * pip

### Install dependencies
```bash
$ sudo apt install -y gcc make build-essential libssl-dev libffi-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev liblzma-dev
```  
### Install codec
```bash
$ sudo apt install libavcodec-dev libavformat-dev libswscale-dev
```  
### Optional dependencies
Please refer to <a href="https://docs.opencv.org/4.x/d2/de6/tutorial_py_setup_in_ubuntu.html">this page.</a>
```bash
sudo apt-get install libpng-dev
sudo apt-get install libjpeg-dev
sudo apt-get install libopenexr-dev
sudo apt-get install libtiff-dev
sudo apt-get install libwebp-dev
```  

### Install FFMPEG
If FFMPEG is not installed, you should install it.  
FFMPEG must be installed before installing opencv-python.  
```bash
$ sudo apt install ffmpeg
```  

### Install Tkinter
```bash
$ sudo apt install python3-tk
```
## Install pyenv
```bash
# Download pyenv
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
Cloning into '/home/user/.pyenv'...
remote: Enumerating objects: 20109, done.
remote: Counting objects: 100% (1021/1021), done.
remote: Compressing objects: 100% (457/457), done.
remote: Total 20109 (delta 627), reused 773 (delta 487), pack-reused 19088
Receiving objects: 100% (20109/20109), 4.10 MiB | 1.89 MiB/s, done.
Resolving deltas: 100% (13562/13562), done.

```  

### Added to .bash_profile and reload
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
```  
```bash: Reload $HOME/.bash_profile
source .bash_profile
```
### make directory
```
$ mkdir ./venv3.7
$ cd ./venv3.7/
```
## Switch interpreter using pyenv
```
$ pyenv install --list

$ pyenv install 3.7.11
$ pyenv local 3.7.11
$ python -V
Python 3.7.11

Upgrade pip
$ pip install -U pip
```

## Switch packages using venv and install packages using pip
```
$ python -m venv ./
$ source bin/activate

Copy requirements.txt from disaster dir to current dir
$ cp ../disaster/requirements.txt ./
$ pip install -r requirements.txt

$ pip freeze
click==8.0.3
dlib==19.22.1
face-recognition==1.3.0
face-recognition-models==0.3.0
Flask==2.0.2
importlib-metadata==4.8.1
itsdangerous==2.0.1
Jinja2==3.0.2
MarkupSafe==2.0.1
numpy==1.21.3
opencv-python==4.5.4.58
Pillow==8.4.0
typing-extensions==3.10.0.2
Werkzeug==2.0.2
zipp==3.6.0
```
## Check if dlib supports cuda
If Dlib does not support cuda, the processing speed will be very slow.  
You must have cuda tool kit, cuBLAS, cuDNN installed before installing Dlib.  
```bash
$ python
Python 3.7.11 (default, Nov  3 2021, 08:07:41) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True
>>> 
```
## Check if opencv-python supports FFMPEG
```bash
$ python -c 'import cv2; print(cv2.getBuildInformation())'
  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES
      avcodec:                   YES (58.91.100)
      avformat:                  YES (58.45.100)
      avutil:                    YES (56.51.100)
      swscale:                   YES (5.7.100)
      avresample:                NO
    GStreamer:                   NO
    v4l/v4l2:                    YES (linux/videodev2.h)
```
