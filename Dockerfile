FROM python:3.6.8
LABEL maintainer="Ali Okan Yuksel <aokany@gmail.com>"
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD [ "python", "./app.py" ]
