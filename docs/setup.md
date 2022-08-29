Installation and Setup
==============

In this page we go over how to setup the application for both development and production.

## Local Installation

To clone the repo and install locally run
```bash
git clone https://github.com/MatrixDoctors/matrix-cerberus.git
cd matrix-cerberus
```

## Development Setup

If you only want to put the application into production, then you can skip this section and go to [production](#production-setup).


## Production Setup

### Configuration files

First comes the configuration files.
This contains all of your sensitive data (i.e third party app IDs and secrets), custom configuration, domain address and other essesntial details which will be required to get your app running properly.

List of configuration and environment files:
- `config.yml` for backend
- `.env.production` for frontend
- `nginx.conf` in `nginx/prod` for nginx


#### 1) Backend configuration (config.yml)

Copy the `config.sample.yml` to a new file `config.yml` and edit the configuration as mentioned in the file.

The current `config.sample.yml` file is configured to be used by the backend tests to test its interactions and functionality.

#### 2) Frontend configuration (.env.production)

Copy the `.env.test` to a new file `.env.production`.

Edit the `REACT_APP_BASE_URL` to the domain url that you intend to host the application on.

You can also optionally edit the `REACT_APP_DEFAULT_HOMESERVER` to view this homeserver by default when the login page loads for the first time.

#### 3) Nginx configuration (nginx.conf)

Copy the `nginx.sample.conf` to a new file `nginx.conf` under the same directory.

Edit the `DOMAIN_URL` to the domain url that you intend to host the application on.

### How to issue SSL certificates for your domain?

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

If you run into any issues while setting up https and certbot, do check out the [article](https://mindsers.blog/post/https-using-nginx-certbot-docker/) or join [#matrix-cerberus:cadair.dev](https://matrix.to/#/#matrix-cerberus:cadair.com) so that we can work out a solution together!
