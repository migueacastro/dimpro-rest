FROM node:23-alpine

WORKDIR /frontend

COPY . .
RUN npm install -g vite
RUN npm install
# RUN npm run buildn

EXPOSE 3000

CMD ["npm", "run", "preview"]
