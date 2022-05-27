# pull official base image
FROM node:16.13.2-alpine

# set working directory
WORKDIR /usr/app

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci

# eslint is present in .cache
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

COPY . .

# start app
CMD ["npm", "run", "start"]