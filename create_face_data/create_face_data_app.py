from os import write
import cv2
import face_recognition
from datetime import datetime
import numpy as np

input_movie = 'people.mp4'
SET_WIDTH = 800
set_area = 'NONE'
upsampling = 0
mode = 'cnn'
jitters = 10
model = 'small'
shelter_name = 'tokyo'


def video_capture(input_movie):
    vcap = cv2.VideoCapture(input_movie, cv2.CAP_FFMPEG)

    if not vcap.isOpened():
        print('Input video data is inappropriate.')
        exit()

    ret, frame = vcap.read()
    if ret == False:
        print('Input video data is inappropriate.')
        exit()

    return vcap, frame


def set_resize(vcap, frame, SET_WIDTH, set_area):
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = int(height)
    width = int(width)

    SET_HEIGHT = int((SET_WIDTH * height) / width)

    TOP_LEFT = (0, int(height/2), 0, int(width/2))
    TOP_RIGHT = (0, int(height/2), int(width/2), width)
    BOTTOM_LEFT = (int(height/2), height, 0, int(width/2))
    BOTTOM_RIGHT = (int(height/2), height, int(width/2), width)
    CENTER = (int(height/4), int(height/4)*3, int(width/4), int(width/4)*3)

    if set_area == 'NONE':
        pass
    elif set_area == 'TOP_LEFT':
        frame = frame[TOP_LEFT[0]:TOP_LEFT[1], TOP_LEFT[2]:TOP_LEFT[3]]
    elif set_area == 'TOP_RIGHT':
        frame = frame[TOP_RIGHT[0]:TOP_RIGHT[1], TOP_RIGHT[2]:TOP_RIGHT[3]]
    elif set_area == 'BOTTOM_LEFT':
        frame = frame[BOTTOM_LEFT[0]:BOTTOM_LEFT[1],
                      BOTTOM_LEFT[2]:BOTTOM_LEFT[3]]
    elif set_area == 'BOTTOM_RIGHT':
        frame = frame[BOTTOM_RIGHT[0]:BOTTOM_RIGHT[1],
                      BOTTOM_RIGHT[2]:BOTTOM_RIGHT[3]]
    elif set_area == 'CENTER':
        frame = frame[CENTER[0]:CENTER[1], CENTER[2]:CENTER[3]]

    small_frame = cv2.resize(frame, (SET_WIDTH, SET_HEIGHT))

    return small_frame


def set_fps(vcap):
    fps = vcap.get(cv2.CAP_PROP_FPS)
    fps = int(fps)


def date_format():
    now = datetime.now()
    return shelter_name + '_' + str(now.year) + '_' + str(now.month) + '_'+str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)

cnt=0
face_encodings_list=[]
name_list =[]
while True:
    vcap, frame = video_capture(input_movie)
    small_frame = set_resize(vcap, frame, SET_WIDTH, set_area)
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_location_list = face_recognition.face_locations(
        small_frame, upsampling, mode)
    face_encodings = face_recognition.face_encodings(
        small_frame, face_location_list, jitters, model)

    name_list.append(date_format())
    face_encodings_list.append(face_encodings[0])

    # for test
    # cv2.imshow('test', small_frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # for test
    cnt=cnt+1
    if cnt > 10000:
        break

np.savez(
    'npKnown',
    name_list,
    face_encodings_list
)
