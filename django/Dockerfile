# pull official base image
FROM python:3.9.4-slim-buster

ENV HOME=/usr/src/app

# set work directory
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update \
    && apt install gcc netcat -y libxml2-dev -y libxslt-dev\
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt $HOME/requirements.txt
RUN pip install -r requirements.txt

RUN python -m nltk.downloader -d /usr/share/nltk_data punkt

# copy project
COPY . /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x ./entrypoint.sh

# run entrypoint.sh 
ENTRYPOINT ["./entrypoint.sh"]
