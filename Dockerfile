FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install catt

ENTRYPOINT ["tail", "-f", "/dev/null"]