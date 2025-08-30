# pull official base image
FROM python:3.10.2-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create virtual env
ENV VIRTUAL_ENV=/usr/venv
RUN python3 -m venv $VIRTUAL_ENV

# create user
#RUN groupadd -r meteo-user &&  \
#    useradd -r -g meteo-user meteo-user && \
#    chown -R meteo-user:meteo-user /usr/venv && \
#    chown -R meteo-user:meteo-user /usr/src/app

# set user
#USER meteo-user
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy app
COPY . .
