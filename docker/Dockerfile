FROM python:3.8-slim-buster

RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgl1 \
    libglib2.0-0 \
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
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV CFLAGS=-static
RUN pip3 install --upgrade pip && \
git clone -b 'v19.21' --single-branch https://github.com/davisking/dlib.git && \
cd dlib/ && \
python3 setup.py install --set BUILD_SHARED_LIBS=OFF

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY ./main.py /app/main.py
COPY . /app

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 443

CMD ["python", "/app/main.py"]
