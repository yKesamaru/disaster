# Build python runtime environment
Here is an example of building a python3.7 runtime environment using `pyenv` and `venv`.
## make directory
```
$ mkdir ./venv3.7
$ cd ./venv3.7/
```
## pyenv
```
$ pyenv install --list

$ pyenv install 3.7.11
$ pyenv local 3.7.11
$ python -V
Python 3.7.11

Upgrade pip
$ pip install -U pip
```

## venv
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