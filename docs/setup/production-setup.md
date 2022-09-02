Production Setup
==============

## Requirements

- Access to a local machine or development server as a non-root user with sudo privileges
- Docker is installed, signed in and running.
   - Installation link: https://docs.docker.com/engine/install/
- Docker compose is installed
  - Installation link: https://docs.docker.com/compose/install/
- Node.js and npm installed
  - Use [nvm](https://github.com/nvm-sh/nvm) to install and manage multiple versions easily.

## Configuration files

First comes the configuration files.
This contains all of your sensitive data (i.e third party app IDs and secrets), custom configuration, domain address and other essesntial details which will be required to get your app running properly.

List of configuration and environment files for production:
- `config.yml` for backend
- `.env.production` for frontend
- `nginx.conf` in `nginx/prod` for nginx


### 1) Backend configuration (config.yml)

You can follow the same instructions mentioned in [here](./development-setup.md#1-backend-configuration-configyml)


### 2) Frontend configuration (.env.production)

Copy the `.env.test` to a new file `.env.production`.

Edit the `REACT_APP_BASE_URL` to the domain url that you intend to host the application on.

You can also optionally edit the `REACT_APP_DEFAULT_HOMESERVER` to view this homeserver by default when the login page loads for the first time.

### 3) Nginx configuration (nginx.conf)

Copy the `nginx.sample.conf` to a new file `nginx.conf` under the same directory (`nginx/prod`).

Edit the `DOMAIN_URL` to the domain url that you intend to host the application on.

## How to issue SSL certificates for your domain?

It is very important to make sure that the application supports HTTPS requests to protect the website and its users from other external factors.

In the docker compose [file](../docker-compose.yml), we've mapped the the local files in certbot directory with other directories which belong to the nginx docker container.

This is to ensure that we keep using the same SSL certificates that has been generated the first time this app has been setup and also to share the data between two different containers i.e. nginx and certbot.

```
  nginx:
    image: "nginx:latest"
    volumes:
      - ./nginx/prod/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./nginx/prod/corsheaders.conf:/etc/nginx/conf.d/corsheaders.conf:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot/:ro
      - ./frontend/build:/usr/src/app
```

```
certbot:
    image: certbot/certbot:latest
    volumes:
      - ./certbot/conf:/etc/letsencrypt:rw
      - ./certbot/www/:/var/www/certbot/:rw
```

Run the following command to fill the `certbot` directory with certificates.

```bash
docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d {DOMAIN_URL}
```

**Note:**
There is a limit to how many certificates can be generated per registered domain. (It is 50 per week)
Please check out <https://letsencrypt.org/docs/rate-limits/>

The generated certificates are only valid for 3 months. To renew the certificates run the command

```
docker-compose run --rm certbot renew
```

If you run into any issues while setting up https and certbot, do check out this [article](https://mindsers.blog/post/https-using-nginx-certbot-docker/) or join [#matrix-cerberus:cadair.dev](https://matrix.to/#/#matrix-cerberus:cadair.com) so that we can work out a solution together!

## Build the React frontend

To use the frontend code in production, we'll have to use the optimized build produced by the `react-scripts` from create-react-app.

But we first need to install the packages before we start building the code.

```
cd frontend/
npm install
```

After the packages have been installed, we can simply run

```
npm run build
```

and we will find a new `build/` directory created.

This will later be served by [Nginx](https://www.nginx.com/resources/wiki/) to the clients requesting it.

## Time to run the application!

Now, that you have everything setup, you can simply start the application by running the commands

```
docker-compose build
docker-compose up
```
