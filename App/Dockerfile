FROM python:3.8

LABEL MAINTAINER Fight Fighters Inc.

ENV APP violence_detection

COPY . /src
WORKDIR /src

RUN apt-get update && apt-get install -y libsnappy-dev
RUN pwd
RUN ls
RUN cat constraints.txt
RUN sudo pip install -r constraints.txt

CMD make launch_app
