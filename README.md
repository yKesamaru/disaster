<div style="text-align: right"><a href="doc/README_ja.md">[ja]</a></div>  

# Disaster
Disaster is a face search system for disasters using `dlib`, `face_recognition`, `flask`, `PySimpleGUI` and others, and what is written in `python`.  

How can you find a loved one in the event of a disaster? Disaster allows you to search for the face of the person you are looking for from the video taken by the camera installed in the shelter.  

Disaster is most privacy-friendly.The face information is replaced with irrecoverable numerical data, and even the developer cannot restore the original face image.  

* Disaster web application demo  
![demo](./img/demo.gif)  
![screenshot](https://user-images.githubusercontent.com/93259837/139792630-06f66eef-2b41-4bbf-8c00-6c57ac811974.png)  

* The Disaster application window demo of creating 128D vector data from faces.  
![create_face_data](./img/demo3.gif)  

## Project background
It is an urgent task to find a solution to situation where safety of a loved one cannot be confirmed in a disaster. 
Currently, various companies are working to solve problems bringing together feasible technologies. 

However, pre-registration before the disaster is often required, and/or family discussions are a prerequisite in advance. 

So it is expected that it will be difficult to confirm the safety of family after the disaster if some measures are not taken before the disaster. 
If the situation when victim cannot be used smartphone, it is so difficult for family to try to contact victim immediately after the disaster. 

These situations are occurring all over the world not only natural disasters but also wars or civil wars.  

## Features
  * Converts the image taken by a camera installed in the shelter into numerical data that cannot be restored to the original face image. Since privacy is of the utmost importance, the victim's face image is not displayed and immediately is removed.

* When upload a family photo to the Disaster web application, it will automatically look for similar faces and display information about when and in which shelter the victim was.  

* Local governments, organizations and others can freely use Disaster.  

## Requirements
* Unix-like OS
* NVIDIA GeForce GTX 1660 Ti +
* Python 3.7 +
* Network camera or webcam
  * Not needed if you just want to try Disaster. In that case, use the attached mp4 file. 
```bash
execution environment (Developer)
Kernel	Linux 5.4.0-89-generic (x86_64)
Version	#100~18.04.1-Ubuntu SMP Wed Sep 29 10:59:42 UTC 2021
C Library	GNU C Library / (Ubuntu GLIBC 2.27-3ubuntu1.4) 2.27
Distribution	Ubuntu 18.04.6 LTS
Renderer	NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2
Version	4.6.0 NVIDIA 470.63.01
AMD Ryzen 5 1400 Quad-Core Processor
Total Memory	16389096 KiB
Python 3.7.11(pyenv)
```
  
## Usage  
```
$ git clone https://github.com/yKesamaru/disaster.git
```
Build python runtime environment and others are described <a href="doc/Build_python_runtime_environment.md">here</a>.

### When trying the Disaster web application
```bash
$ cd web_app
$ export FLASK_APP=main.py
$ flask run
 * Serving Flask app 'main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
*** Access `http://127.0.0.1:5000/` ***

### When trying to create numerical face data
You can use network cameras and USB cameras in Disaster.  
Here, an mp4 file is used for the sake of simplicity.  
Optional: Activate the Python virtual environment in advance.
```bash
$ cd create_face_data/shelter01
$ python create_face_data_app.py 
$ cd ../
$ python marge_npKnown.py
```

## Component
This system consists of three blocks.
### 1. Web application  
![web_application](https://user-images.githubusercontent.com/93259837/139513838-3e22fb8e-f9b7-4c88-aa7c-2ec4aa72cdd4.png)  
```bash
Disaster
└ web_app
    ├ main.py
    ├ npKnown.npz
    └ others
```
People who want to find a family upload a family photo. It converts to non-recoverable numerical data on the server and searches for similar faces in the footage taken by the shelter's camera. Date, time and the shelter's name are displayed on the smartphone.  

### 2. The Application for creating numerical face data from camera
![make_data_application](https://user-images.githubusercontent.com/93259837/139513900-7dd066a4-5295-4ae6-aa49-d3e6feb01cd6.png)  
```bash
Disaster
└ create_face_data
    ├ marge_npKnown.py
    ├ npKnown_root.npz
    ├ shelter01
    │  ├ create_face_data_app.py
    │  ├ shelter01.mp4    
    │  └ npKnown.npz
    └ shelter02
        ├ create_face_data_app.py
        ├ shelter02.mp4    
        └ npKnown.npz
```
All the faces taken by the camera installed in the shelter are converted into numerical data.  

The shelter01 and shelter02 directories were created to represent multiple shelters.  
Click <a href="doc/How_to_operate.md">here</a> for a more detailed explanation.

### 3. Data synchronization between servers
The face data file is shared between each server to prevent the entire system from going down.  

## Project maintenance and contribution
Disaster is maintenanced by Yoshitsugu Kesamaru.  
I hope that similar projects will spread widely.  

My mother tongue is not English, so I'm not very good at English, so I would appreciate it if you could point out any description using incorrect English. 

Thankyou

## ToDo
* Make it easier to build an environment using Docker.

