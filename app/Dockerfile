# pull official base image
FROM python:3.8.0-alpine

ENV HOME=/usr/src/app

# set work directory
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev 

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt $HOME/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
# COPY . /usr/src/app/

# run entrypoint.sh 
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]       
