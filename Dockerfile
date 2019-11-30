FROM node:10

WORKDIR /usr/src/app

COPY package*.json ./

RUN yarn
COPY . .

CMD [ "node", "setup_predict.js" ]