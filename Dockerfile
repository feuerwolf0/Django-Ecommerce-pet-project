FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
EXPOSE 8000

COPY ./requirements.txt /usr/src/app/req.txt
COPY . /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/req.txt

RUN adduser --disabled-password django-user

USER django-user


