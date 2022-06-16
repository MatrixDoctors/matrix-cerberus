FROM python:3.10

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install 'uvicorn[standard]'

COPY . .

# start app
CMD ["python", "./run.py"]
