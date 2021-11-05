import os
import shutil

import numpy as np


def find_all_files(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if 'npKnown.npz' in file:
                yield os.path.join(root, file)


def load_npKnown(file):
    npKnown = np.load(file, allow_pickle=True)
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

    return known_face_names_list, known_face_encodings_list


extend_known_face_names_list = []
extend_known_face_encodings_list = []
file_list = []
for file in find_all_files('.'):
    # print(file)
    file_list.append(file)

for file in file_list:
    known_face_names_list, known_face_encodings_list = load_npKnown(file)
    extend_known_face_names_list.extend(known_face_names_list)
    extend_known_face_encodings_list.extend(known_face_encodings_list)

np.savez(
    'npKnown_root',
    extend_known_face_names_list,
    extend_known_face_encodings_list
)

shutil.copy2("npKnown_root.npz", "../web_app/npKnown.npz")
