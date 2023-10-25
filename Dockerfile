FROM python:3.12.0-alpine3.18

WORKDIR /usr/src/app

COPY secret_santa secret_santa/
COPY datasets datasets/

CMD "sh"
