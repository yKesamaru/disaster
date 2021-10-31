import os
from flask import (Flask, render_template, request)
import cv2
import face_recognition
from PIL import Image
import numpy as np
import random

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route('/')
def index():
    return render_template(
        'index.html'
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


@app.route('/uploads', methods=['get', 'post'])
def send():
    img_file = request.files['img_file']
    img_file.save(os.path.join(UPLOAD_FOLDER, img_file.filename))

    check_images_file_npData = cv2.imread(
        os.path.join(UPLOAD_FOLDER, img_file.filename))

    # BGRからRGBへ変換
    check_images_file_npData = check_images_file_npData[:, :, ::-1]

    # face_locationsを算出
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

    if len(face_locations) > 0:
        return render_template(
            'send.html',
            face_locations=face_locations,
            face_file_name_list=face_file_name_list
        )
    else:
        return render_template('index.html')


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
    # matches = face_recognition.compare_faces(known_face_encodings_ndarray, face_encoding, 0.80)
    face_distances = face_recognition.face_distance(
        known_face_encodings_ndarray, face_encoding)
    best_match_index = np.argmin(face_distances)
    shelter_name = "couldn't find that person"
    date = 'None'
    if matches[best_match_index]:
        shelter_name = known_face_names_list[best_match_index]
        print('sheltername is ', shelter_name)
        shelter_name, date = shelter_name.split('_', maxsplit=1)
    return render_template(
        'search_result.html',
        name=name,
        shelter_name=shelter_name,
        date=date
    )
