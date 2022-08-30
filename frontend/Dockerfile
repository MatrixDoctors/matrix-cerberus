#This Dockerfile will be used only during development mode.
#During production, the build folder is automatically served by the nginx server.

# pull official base image
FROM node:16.13.2-alpine
ENV NODE_ENV development

# set working directory
WORKDIR /frontend

# install and cache app dependencies
COPY package.json /frontend
COPY package-lock.json /frontend
RUN npm ci && npm cache clean --force

# start app
CMD ["npm", "run", "start"]
