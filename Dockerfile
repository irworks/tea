# syntax=docker/dockerfile:1
FROM node:latest AS builder
WORKDIR /app
COPY /app .

RUN npm install && npm run production

FROM python:3.9.9-slim-bullseye
WORKDIR /python-docker

COPY . .
COPY --from=builder /app ./app/

RUN pip3 install -r requirements.txt

CMD [ "python3", "__main__.py" ]