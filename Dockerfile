FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir /app/repo

ADD . /app 

RUN apt-get update && apt-get install -y git

RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "events2git.py" ]