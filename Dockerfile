FROM python:3.10-slim

WORKDIR /draft_fifa


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
