FROM python:3.8.13-alpine3.16
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN apk add -u gcc musl-dev
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
