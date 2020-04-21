FROM node:8.15.1-alpine

EXPOSE 9000

ENV APP_PATH /usr/share/app

RUN mkdir -p $APP_PATH && chown node:node $APP_PATH

WORKDIR $APP_PATH

USER node

COPY . $APP_PATH/

RUN npm install

CMD ["npm", "start"]

