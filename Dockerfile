FROM ubuntu:18.04
LABEL maintainer="yKesamaru <y.kesamaru@tokai-kaoninsho.com>"

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

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
    # python3-opencv \
    ffmpeg \
    libpng-dev \
    libopenexr-dev \
    libwebp-dev \
    python3-setuptools \
    python3-pip \
    python-pip-whl \
    python3-tk \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Install dlib
RUN cd ~ && \
    mkdir -p dlib && \
    # git clone -b 'v19.22' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    git clone https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install

# Install Disaster
RUN mkdir /root/disaster/

COPY . /root/disaster

RUN cd  /root/disaster/ && \
    pip3 install -U pip && \
    pip3 install -r requirements.txt

CMD export LC_ALL=C.UTF-8 && \
    export LANG=C.UTF-8 && \
    cd /root/disaster/create_face_data/shelter01/ && \
    python3 ./create_face_data_app.py && \
    cd /root/disaster/web_app/ && \
    export FLASK_APP=main.py && \
    # flask run --host=0.0.0.0 && \
    flask run --host=0.0.0.0


