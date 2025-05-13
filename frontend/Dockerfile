FROM node:23-alpine

WORKDIR /frontend

COPY . .
RUN npm install -g vite
RUN npm install
RUN npm i svelte-check --save-dev
EXPOSE 3000
