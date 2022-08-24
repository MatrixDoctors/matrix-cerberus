FROM python:3.10

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install 'uvicorn[standard]'

ARG CONFIG_FILE

COPY ./app ./app
COPY ${CONFIG_FILE} ${CONFIG_FILE}

ENV CONFIG_FILE=${CONFIG_FILE}

# start app
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
