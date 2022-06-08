#This Dockerfile will be used only during development mode.
#During production, the build folder is automatically served by the nginx server.

# pull official base image
FROM node:16.13.2-alpine
ENV NODE_ENV production

# set working directory
WORKDIR /usr/app

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci && npm cache clean

COPY . .

# start app
CMD ["npm", "run", "start"]