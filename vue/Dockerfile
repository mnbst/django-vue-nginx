FROM node:13.3-alpine

RUN apk add --update nodejs npm                

# set work directory
WORKDIR /usr/src/app

# copy project
COPY . .

CMD [ "npm","run","serve"]