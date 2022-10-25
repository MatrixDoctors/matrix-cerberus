Development Setup
==============

This is for those who intend to contribute to this project (thank you!) or would like to play around a bit with the app by setting it up locally.

## Requirements

- Docker is installed, signed in and running.
   - Link to installation - https://docs.docker.com/engine/install/
- Docker compose is installed
  - Link to installation - https://docs.docker.com/compose/install/

## Configuration files

The configuration files are similar to the ones in production except for a few changes.

List of configuration and environment files for development:
- `config.yml` for backend
- `.env.development` for frontend

### 1) Backend configuration (config.yml)

Copy the `config.sample.yml` to a new file `config.yml` and edit the configuration as mentioned in the file.

The current `config.sample.yml` file is configured to be used by the backend tests to test its interactions and functionality.

### 2) Frontend configuration (.env.development)

Copy the following into a new file `.env.development`.

```
REACT_APP_BASE_URL=http://localhost:80
REACT_APP_DEFAULT_HOMESERVER=https://matrix.org
WDS_SOCKET_PORT=0
```
**Note:**

The last variable `WDS_SOCKET_PORT` is used to avoid the following error.
```
Browser can’t establish a connection to the server at ws://localhost:3000/ws.
```
We lose the hot reloading feature in this case. You can find more details about it [here](https://github.com/facebook/create-react-app/issues/11779).

## Running the application

There are two different `docker-compose` files available, one for development (`docker-compose-dev.yml`) and one for production (`docker-compose.yml`).

By default, docker-compose uses the `docker-compose.yml` file.
Use the `-f` flag to specify the filename

Run the following commands to start the application
```
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up
```

You can find the application running here [localhost:80/](http://localhost:80/)
