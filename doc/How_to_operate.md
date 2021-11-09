# How to operate Disaster application
## create_face_data_app.py
create_face_data_app.py creates 128D vector data from the face in the camera.  
Directory structure is as follows.
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
In create_face_data_app.py, the behavior is controlled by the following parts. 
```python
# Initialize
input_movie = 'shelter01.mp4'
SET_WIDTH = 700
set_area = 'NONE'
SET_FPS = 10
FRAME_DROP = 3
upsampling = 0
mode = 'cnn'
jitters = 0
model = 'small'
shelter_name = 'Tokyo 1st community disaster center'
phone_number = '&#128241; <a href="tel:123-45-6789">123-45-6789</a>'
location = '<iframe src="https://maps.google.co.jp/maps?output=embed&q=東京駅&z=16" width="70%" frameborder="0" scrolling="no" ></iframe>'
```
### input_movie
Specify the input video source in the part of `input_movie`.  
Since FFMPEG is used in the background of opencv-python, you can use a network camera that supports HLS.  
It may be more convenient to specify gstreamer in the background of opencv-python.  
Here, the input video is an mp4 file for the sake of simplicity.  
### SET_FPS, FRAME_DROP
`SET_FPS` cannot be used if the input video is a video file such as an mp4 rather than a webcam or network camera.
Therefore, if the processing speed is slow, use `FRAME_DROP` to control it.
### SET_WIDTH, set_area
Resize the input video to the appropriate size.Input video that is too large will be a burden on the processor.However, if `SET_WIDTH` is made too small, the face area will become too small and it will not be recognized as a face.The area of the face must be 80x80px or more.If you cannot move the camera position by all means, you can use only a specific part of the input video by specifying `set_area`.Please note that the resolution will drop.  
### upsampling, mode, jitters
By changing `upsampling` from 0 to 1, you can change the recognized face area from 80x80px to 40x40px.Please note that the processing speed will be slower instead.  
Changing `mode` from` cnn` to `hog` may improve processing speed, but it will not be able to recognize the masked face.Try it on a device that doesn't install the NVIDIA GPU card.  
You can change the `jitters` to slightly improve the face recognition rate. Please note that the processing speed will be slower. 
### model
If you change from `small` to` large`, the face recognition rate will increase slightly, but the processing speed will decrease.
### shelter_name, phone_number, location
The information of shelter is described.  
