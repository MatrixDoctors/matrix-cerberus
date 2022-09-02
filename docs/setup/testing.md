Testing
==============

Currently, there is no support for running tests in docker. So, you will have to setup the dependencies in your system manually.

## Requirements

- [Redis](https://redis.io/) is installed and running
    - Installation link: https://redis.io/docs/getting-started/installation/install-redis-on-linux/
- It is recommended to use `venv` (virtual environment) to install the project depenendencies. This helps avoid conflicts globally.

## Backend tests

We use `pytest` to test our backend framework.
Run the following commands to start running all the tests

```
cd backend/
pytest
```

**Note:**
Make sure to activate the virtual environment incase you are using before you run the above commands.

## Frontend tests

We use the testing framework provided by the [react-testing-library](https://www.google.com/search?channel=fs&client=ubuntu&q=react+testing+library) and Jest runner to test the frontend code.

Run the following commands to start the tests
```
cd frontend/
npm run test
```
