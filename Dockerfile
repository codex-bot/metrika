FROM python:3.9-slim-buster


WORKDIR /home/metrika

RUN pip install --upgrade pip
COPY ./requirements.txt /home/metrika/requirements.txt
RUN pip install -r requirements.txt

COPY . .