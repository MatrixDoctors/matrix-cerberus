# matrix-cerberus

**matrix-cerberus** is an application that has the ability to delegate membership of a room based on a user’s interaction with other third party services.

## Features (In progress)
- Send automatic invites to authorized users.
- Update membership based on user's present status (Invite, Kick)
- Admin panel for configuring relationships between rooms and users.
- Generate external invite URLs for a room.
- Token authenticated registration for a particular server.

## Supported third party accounts
- GitHub
- Patreon

## Development Setup

1) To clone the repo and install locally run
    ```bash
    git clone https://github.com/MatrixDoctors/matrix-cerberus.git
    cd matrix-cerberus
    ```

2) Install the required libraries for both frontend and backend

    ```bash
    # frontend
    cd frontend
    npm install

    cd ..

    # for backend
    cd backend
    pip install -r requirements.txt

    cd ..
    ```

    Note: It is recommended to use a virtual environment `venv` to install the packages in python.

3) Build and run the containers in docker
    ```bash
    sudo docker-compose build
    sudo docker-compose up
    ```

4) Now, try opening `localhost:80` in your browser to access the application.

5) You can access the api docs for FastAPI backend at `localhost:80/api/docs`
