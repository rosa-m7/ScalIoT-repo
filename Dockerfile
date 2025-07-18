FROM python:3.11-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "-m", "flask", "--app", "my-app/run", "run", "--host=0.0.0.0", "--port=8080"]
