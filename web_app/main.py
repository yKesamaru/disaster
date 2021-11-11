import os
import random
import shutil

import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
import werkzeug

# ToDo
# Check uploaded file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limit upload file size : 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

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


@app.route('/')
def index():
    # initialize -----
    # remove /static/faces/*
    shutil.rmtree('static/faces/')
    os.mkdir('static/faces/')
    # ----------------
    return render_template(
        'index.html'
    )


@app.route('/too_large_file')
def too_large_file():
    return render_template(
        'too_large_file.html'
    )


@app.route('/upload_page')
def goto_upload_page():
    return render_template(
        'upload_page.html'
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


@app.route('/uploads', methods=['get', 'post'])
def send():
    img_file = request.files['img_file']
    uploaded_file_path = os.path.join(
        UPLOAD_FOLDER, secure_filename(img_file.filename))
    # uploaded_file_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
    img_file.save(uploaded_file_path)

    check_images_file_npData = cv2.imread(
        os.path.join(UPLOAD_FOLDER, secure_filename(img_file.filename)))

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


@app.route('/static/faces/<name>.html')
def name_path(name):
    name_path = 'static/faces/' + name
    selected_face_npData = cv2.imread(name_path)
    face_location = face_recognition.face_locations(
        selected_face_npData, 0, 'cnn')
    face_encoding = face_recognition.face_encodings(
        selected_face_npData, face_location, 0, 'small')

    matches = face_recognition.compare_faces(
        known_face_encodings_ndarray, face_encoding, 0.35)
    # matches = face_recognition.compare_faces(known_face_encodings_ndarray, face_encoding, 0.45)
    face_distances = face_recognition.face_distance(
        known_face_encodings_ndarray, face_encoding)
    best_match_index = np.argmin(face_distances)
    shelter_name = "couldn't find that person"
    date = 'None'
    if matches[best_match_index]:
        shelter_name = known_face_names_list[best_match_index]
        print('sheltername is ', shelter_name)
        shelter_name, date = shelter_name.split('__', maxsplit=1)

    return render_template(
        'search_result.html',
        name = name,
        shelter_name = shelter_name,
        date = date
    )
