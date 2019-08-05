FROM python:3.7.3-slim-stretch

WORKDIR /src/app
COPY requirements.txt requirements.txt
RUN set -x &&
    pip install -U pip && \
    pip install -r /src/app/requirements.txt && \
    rm /src/app/requirements.txt