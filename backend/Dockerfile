FROM python:3.10

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install 'uvicorn[standard]'

COPY ./app ./app
COPY "config.yml" "config.yml"

# start app
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
