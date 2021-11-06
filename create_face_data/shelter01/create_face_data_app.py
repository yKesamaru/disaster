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

input_movie = 'shelter01.mp4'
SET_WIDTH = 600
set_area = 'NONE'
SET_FPS = 10
FRAME_DROP = 1
upsampling = 0
mode = 'cnn'
jitters = 0
model = 'small'
shelter_name = 'tokyo 1st community disaster center'
phone_number = '&#128241; <a href="tel:123-45-6789">123-45-6789</a>'
location = '<iframe src="https://maps.google.co.jp/maps?output=embed&q=東京駅&z=16" width="70%" frameborder="0" scrolling="no" ></iframe>'

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

logo_image = cv2.imread("images/logo.png", cv2.IMREAD_UNCHANGED)
rect01_image = cv2.imread("images/rect01.png", cv2.IMREAD_UNCHANGED)


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

    alpha = 0.3
    overlay = small_frame.copy()
    orgHeight, orgWidth = logo_image.shape[:2]
    ratio = SET_WIDTH / orgWidth / 4  # テロップ幅は横幅の半分に設定
    logo_image = cv2.resize(logo_image, None, fx=ratio, fy=ratio)
    x1, y1, x2, y2 = 0, 0, logo_image.shape[1], logo_image.shape[0]
    try:
        small_frame[y1:y2, x1:x2] = small_frame[y1:y2, x1:x2] * \
            (1 - logo_image[:, :, 3:] / 255) + \
            logo_image[:, :, :3] * (logo_image[:, :, 3:] / 255)
    except:
        pass

    event, _ = window.read(timeout=1)

    imgbytes = cv2.imencode(".png", small_frame)[1].tobytes()
    window["display"].update(data=imgbytes)
    if event == 'terminate':
        break

    face_location_list = face_recognition.face_locations(
        small_frame, upsampling, mode)

    # < BUG > -------------------------------------------------
    if len(face_location_list) > 0:
        (top, right, bottom, left) = face_location_list[0]
        face_width = right - left
        face_height = bottom - top
        rect_orgHeight, rect_orgWidth = rect01_image.shape[:2]
        width_ratio = 1.0 * (face_width / rect_orgWidth)
        height_ratio = 1.0 * (face_height / rect_orgHeight)
        rect01_image = cv2.resize(
            rect01_image, None, fx=width_ratio, fy=height_ratio)
        rect01_x1, rect01_y1, rect01_x2, rect01_y2 = left, top, left + \
            rect01_image.shape[1], top + rect01_image.shape[0]
        try:
            small_frame[rect01_y1:rect01_y2, rect01_x1:rect01_x2] = small_frame[rect01_y1:rect01_y2, rect01_x1:rect01_x2] * \
                (1 - rect01_image[:, :, 3:] / 255) + \
                rect01_image[:, :, :3] * (rect01_image[:, :, 3:] / 255)
        except:
            print('描画できない')
            pass
    # ---------------------------------------------------------

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
        cnt = 0
    # ----------------------------------------------

vcap.release()
cv2.destroyAllWindows()

np.savez(
    'npKnown',
    name_list,
    face_encodings_list,
)
