FROM python:3.8-slim-buster

COPY . /src

WORKDIR /src

RUN pip install -e .[dev,test]

#RUN useradd -u 8877 caleb
#USER caleb
