FROM node:14-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@7.24.0
RUN apk add --update python3 make g++ && rm -rf /var/cache/apk/*
RUN npm i
COPY . ./
RUN ls -la
CMD npm run build

ENV PUBLIC_URL='/'
CMD npm install -g serve && serve -s build