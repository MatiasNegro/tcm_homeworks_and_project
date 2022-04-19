# syntax=docker/dockerfile:1
FROM ubuntu
COPY . .
RUN apt-get update -y && \
    apt install python -y  && \
    pip install boto3
WORKDIR /app
CMD python main.py;
EXPOSE 3000