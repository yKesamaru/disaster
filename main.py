import os
import random
import shutil

import cv2
import face_recognition
import numpy as np
import werkzeug
from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename

# ToDo
# Check uploaded file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# limit upload file size : 16MB
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# However, when demonstrating on heroku, the memory allocation is very small, so limit it to less than 300KB.
# app.config['MAX_CONTENT_LENGTH'] = 300 * 1024
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024

# Max image size
HEIGHT = 800
WIDTH = 800

npKnown = np.load('npKnown.npz', allow_pickle=True)
A, B = npKnown.files
known_face_names_ndarray = npKnown[A]
known_face_encodings_ndarray = npKnown[B]

# from ndarray to list ----
known_face_names_list = known_face_names_ndarray.tolist()
list = []
for i in known_face_encodings_ndarray:
    list.append(i)
known_face_encodings_list = list
# -------------------------


@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    # print("werkzeug.exceptions.RequestEntityTooLarge")
    return render_template(
        'too_large_file.html'
    )

from werkzeug.exceptions import HTTPException


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("error.html", e=e), 500

@app.route('/')
def index():
    # initialize -----
    # remove /static/faces/*
    shutil.rmtree('static/faces/')
    os.mkdir('static/faces/')
    f = open('static/faces/tmp.txt', 'w')
    f.close()
    # ----------------
    return render_template(
        'index.html'
    )

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.route('/too_large_file')
def too_large_file():
    return render_template(
        'too_large_file.html'
    )

@app.route('/information')
def information():
    return render_template(
        'information.html'
    )

@app.route('/individual')
def individual():
    return render_template(
        'individual.html'
    )

@app.route('/enterprise')
def enterprise():
    return render_template(
        'enterprise.html'
    )

@app.route('/organization')
def organization():
    return render_template(
        'organization.html'
    )

@app.route('/heroku_photos')
def heroku_photos():
    return render_template(
        'heroku_photos.html'
    )

@app.route('/upload_page')
def goto_upload_page():
    return render_template(
        'upload_page.html'
    )

@app.route('/more_details')
def more_details():
    return render_template(
        'more_details.html'
    )

@app.route('/terms_n_conditions')
def terms_n_conditions():
    return render_template(
        'terms_n_conditions.html'
    )


@app.route('/no_face')
def no_face():
    return render_template(
        'no_face.html'
    )

def scale_box(img, WIDTH, HEIGHT):
    """Fix the aspect ratio and resize it so that it fits in the specified size.
    """
    height, width = img.shape[:2]
    aspect = width / height
    if WIDTH / HEIGHT >= aspect:
        nh = HEIGHT
        nw = round(nh * aspect)
    else:
        nw = WIDTH
        nh = round(nw / aspect)
    dst = cv2.resize(img, dsize=(nw, nh))
    return dst

@app.route('/uploads', methods=['get', 'post'])
def send():
    img_file = request.files['img_file']

    uploaded_file_path = os.path.join(
        UPLOAD_FOLDER, secure_filename(img_file.filename))
    # uploaded_file_path = os.path.join(UPLOAD_FOLDER, img_file.filename)

    img_file.save(uploaded_file_path)

    check_images_file_npData = cv2.imread(
        os.path.join(UPLOAD_FOLDER, secure_filename(img_file.filename)))

    check_images_file_npData = scale_box(check_images_file_npData, WIDTH, HEIGHT)

    # convert BGR to RGB
    check_images_file_npData = check_images_file_npData[:, :, ::-1]
    # < test > -------
    # import PySimpleGUI as sg
    # layout = [
    #     [sg.Image(filename='', key='display', pad=(0, 0))],
    #     [sg.Button('terminate', key='terminate', pad=(0, 10))]
    # ]
    # window = sg.Window(
    #     'Disaster test', layout, alpha_channel=1, margins=(0, 0),
    #     grab_anywhere=True,
    #     location=(350, 130), modal=True
    # )
    # while True:
    #     event, _ = window.read(timeout=1)
    #     check_images_file_npData = cv2.resize(check_images_file_npData, dsize=(700, 700))
    #     imgbytes = cv2.imencode(".png", check_images_file_npData)[1].tobytes()
    #     window["display"].update(data=imgbytes)
    #     if event == 'terminate':
    #         break
    #     if event == sg.WIN_CLOSED:
    #         break
    # window.close()
    # ----------------

    face_locations = face_recognition.face_locations(
        check_images_file_npData, 0, 'cnn')
    face_file_name_list = []
    for (top, right, bottom, left) in face_locations:
        img = Image.fromarray(check_images_file_npData)
        imgCroped = img.crop(
            (left - 20, top - 20, right + 20, bottom + 20)).resize((200, 200))
        rand = random.randint(0, 100)
        face_file_name = 'static/faces/' + str(rand) + img_file.filename
        face_file_name_list.append(face_file_name)
        imgCroped.save(face_file_name)

    # remove uploaded photo image file
    os.remove(uploaded_file_path)

    if len(face_locations) > 0:
        return render_template(
            'send.html',
            face_locations=face_locations,
            face_file_name_list=face_file_name_list
        )
    else:
        return render_template('no_face.html')

def to_percentage(tolerance):
    # str型で渡されてもいいようにfloatに型変換
    tolerance = float(tolerance)
    percentage = -4.76190475*(tolerance * tolerance)+(-0.380952375) * tolerance +100
    return percentage

@app.route('/static/faces/<name>.html')
def name_path(name):
    name_path = 'static/faces/' + name
    selected_face_npData = cv2.imread(name_path)
    face_location = face_recognition.face_locations(
        selected_face_npData, 0, 'cnn')
    face_encoding = face_recognition.face_encodings(
        selected_face_npData, face_location, 0, 'small')

    try:
        matches = face_recognition.compare_faces(
            known_face_encodings_ndarray, face_encoding, 0.35)
        # matches = face_recognition.compare_faces(known_face_encodings_ndarray, face_encoding, 0.45)
    except:
        return render_template('error.html', name=name)

    face_distances = face_recognition.face_distance(
        known_face_encodings_ndarray, face_encoding)
    best_match_index = np.argmin(face_distances)
    shelter_name = "couldn't find that person"
    date = 'None'
    percentage = ''
    if matches[best_match_index]:
        shelter_name = known_face_names_list[best_match_index]
        shelter_name, date = shelter_name.split('__', maxsplit=1)
        percentage = to_percentage(min(face_distances))
        percentage = str(round(percentage, 2)) + '%'
        print('percentage: ', percentage)

    return render_template(
        'search_result.html',
        name = name,
        shelter_name = shelter_name,
        date = date,
        percentage = percentage
    )
