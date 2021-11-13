# This sample Dockerfile was created with reference to ageitgey/face_recognition.

FROM python:3.9.8-bullseye

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    python3-opencv \
    ffmpeg \
    libpng-dev \
    libopenexr-dev \
    libwebp-dev \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Install dlib
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Install Disaster
COPY . /root/disaster
RUN cd  /root/disaster/ && \
    pip3 install -r requirements.txt

CMD cd /root/disaster/web_app/ && \
    export FLASK_APP=main.py && \
    flask run --host=0.0.0.0
