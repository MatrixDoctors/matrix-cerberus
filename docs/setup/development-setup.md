Development Setup
==============

This is for those who intend to contribute to this project (thank you!) or would like to play around a bit with the app by setting it up locally.


## Configuration files

The configuration files are similar to the ones in production except for a few changes.

List of configuration and environment files for development:
- `config.yml` for backend
- `.env.development` for frontend

### 1) Backend configuration (config.yml)

You can follow the same instructions mentioned in [here](#1-backend-configuration-configyml)

### 2) Frontend configuration (.env.development)

Copy the following into a new file `.env.development`.

```
REACT_APP_BASE_URL=http://localhost:80
REACT_APP_DEFAULT_HOMESERVER=https://matrix.org
WDS_SOCKET_PORT=0
```
