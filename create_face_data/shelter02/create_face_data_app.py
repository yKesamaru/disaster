import shutil
from datetime import datetime

import cv2
import face_recognition
import numpy as np
import PySimpleGUI as sg

# for test ---
# import sys
# import pprint
# pprint.pprint(sys.path)
# ------------

input_movie = 'shelter02.mp4'
SET_WIDTH = 600
set_area = 'NONE'
SET_FPS = 10
FRAME_DROP = 1
upsampling = 0
mode = 'cnn'
jitters = 0
model = 'small'
shelter_name = 'osaka 3rd hospital'
phone_number = '&#128241; <a href="tel:786-78-9123">456-78-9123</a>'
location = '<iframe src="https://maps.google.co.jp/maps?output=embed&q=大阪駅&z=16" width="70%" frameborder="0" scrolling="no" ></iframe>'

adress = shelter_name + '<br>' + phone_number + '<br>' + location


def set_resize(vcap, frame, SET_WIDTH, set_area):
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height = int(height)
    # width = int(width)

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
    # If the input source is a camera, 'set' can be used.
    is_success = vcap.set(cv2.CAP_PROP_FPS, SET_FPS)
    return is_success


def date_format():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)

    return adress + '_' + day + '/' + month + '/' + year + ', ' + hour + '.' + minute


sg.theme('Reddit')

layout = [
    [sg.Text('Disaster sample window')],
    [sg.Image(key='display')],
    [sg.Button('terminate', key='terminate', button_color='red')]
]

window = sg.Window('Disaster sample window', layout)


cnt = 0
fps_counter = 0
save_counter = 0
face_encodings_list = []
name_list = []

vcap = cv2.VideoCapture(input_movie, cv2.CAP_FFMPEG)
if not vcap.isOpened():
    print('Input video data is not opened.')
    exit()

while True:
    ret, frame = vcap.read()
    if ret == False:
        print('Input video data cannot read.')
        break

    is_success = set_fps(vcap)
    # set fps --------
    if is_success == False:
        fps_counter += 1
        if fps_counter < FRAME_DROP:
            continue
        fps_counter = 0
    # ----------------
    small_frame = set_resize(vcap, frame, SET_WIDTH, set_area)
    # small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    event, _ = window.read(timeout=1)

    imgbytes = cv2.imencode(".png", small_frame)[1].tobytes()
    window["display"].update(data=imgbytes)
    if event == 'terminate':
        break

    face_location_list = face_recognition.face_locations(
        small_frame, upsampling, mode)
    face_encodings = face_recognition.face_encodings(
        small_frame, face_location_list, jitters, model)

    try:
        name_list.append(date_format())
        face_encodings_list.append(face_encodings[0])
    except:
        pass

    # For updating npKnown.npz from time to time. --
    cnt = cnt+1
    if cnt > 100:
        save_counter += 1
        print('save: ', save_counter)
        np.savez(
            'npKnown',
            name_list,
            face_encodings_list
        )
        # shutil.copy2("npKnown.npz", "../web_app/npKnown.npz")
        cnt = 0
    # ----------------------------------------------

vcap.release()
cv2.destroyAllWindows()

np.savez(
    'npKnown',
    name_list,
    face_encodings_list,
)
# shutil.copy2("npKnown.npz", "../web_app/npKnown.npz")