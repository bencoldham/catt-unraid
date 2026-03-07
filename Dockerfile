FROM python:3.12-slim

# Env setup.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local"
WORKDIR /app
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Create a symlink pointing expected catt config ->  unraid config
RUN mkdir -p /root/.config
RUN ln -s /config /root/.config/catt

# Run container.
COPY src/ .
EXPOSE 5000
CMD ["python", "main.py"] 