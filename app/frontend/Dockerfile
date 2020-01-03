FROM node:13.3-alpine

RUN apk update \
    && apk add --update nodejs npm \
    && npm install -g yarn  
    #&& npm install -g @vue/cli@latest               

# set work directory
WORKDIR /usr/src/app/frontend

# copy project
COPY . .

CMD [ "yarn","serve" ]