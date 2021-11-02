from os import write
import cv2
import face_recognition
from datetime import datetime
import numpy as np

# for test ---
# import sys
# import pprint
# pprint.pprint(sys.path)
# ------------

input_movie = 'people.mp4'
SET_WIDTH = 800
set_area = 'NONE'
SET_FPS = 10
upsampling = 0
mode = 'cnn'
jitters = 0
model = 'small'
shelter_name = 'tokyo 1st community disaster center'
phone_number = '&#128241; <a href="tel:123-45-6789">123-45-6789</a>'
location = '<iframe src="https://maps.google.co.jp/maps?output=embed&q=東京駅&z=16" width="70%" frameborder="0" scrolling="no" ></iframe>'

adress = shelter_name + '<br>' + phone_number + '<br>' + location


def video_capture(input_movie):
    vcap = cv2.VideoCapture(input_movie, cv2.CAP_FFMPEG)

    if not vcap.isOpened():
        print('Input video data is inappropriate.')
        exit()

    ret, frame = vcap.read()
    if ret == False:
        print('Input video data is inappropriate.')
        exit()

    # vcap.set(cv2.CAP_PROP_FPS, SET_FPS)

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
    return fps


def date_format():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)

    return adress + '_' + day + '/' + month + '/' + year + ', ' + hour + '.' + minute


cnt = 0
fps_counter = 0
save_counter = 0
face_encodings_list = []
name_list = []
while True:
    vcap, frame = video_capture(input_movie)
    # set fps --------
    if fps_counter < 3:
        fps_counter = fps_counter + 1
        continue
    fps_counter = 0
    # ----------------
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
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     break

    # for test
    cnt = cnt+1
    if cnt > 100:
        save_counter =+ 1
        print('save: ', save_counter)
        np.savez(
            'npKnown',
            name_list,
            face_encodings_list
        )
        cnt = 0

np.savez(
    'npKnown',
    name_list,
    face_encodings_list,
)
