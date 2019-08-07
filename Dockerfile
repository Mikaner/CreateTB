FROM python:3.7.3

WORKDIR /src/app
RUN apt update
RUN apt -y install ffmpeg

COPY requirements.txt requirements.txt
RUN set -x && \
    pip install -U pip && \
    pip install -r /src/app/requirements.txt && \
    rm /src/app/requirements.txt