FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install catt

ENTRYPOINT ["tail", "-f", "/dev/null"]

# Create a symlink pointing expected catt config ->  unraid config
RUN mkdir -p /root/.config
RUN ln -s /config /root/.config/catt

COPY main.py /app/main.py
WORKDIR /app

EXPOSE 5000
CMD ["python", "main.py"]