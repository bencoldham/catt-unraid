# Variables
IMAGE_NAME = bencoldham/catt-unraid
VERSION = 0.0.1
DOCKER_DIR = docker
DOCKERFILE = $(DOCKER_DIR)/Dockerfile
COMPOSE_FILE = $(DOCKER_DIR)/docker-compose.yml

# Testing/clean-up
.PHONY: run clean build push help

# Testing/clean-up.	
.PHONY: run clean
run:
	docker compose -f $(COMPOSE_FILE) down
	rm -rf ./config_test
	mkdir ./config_test
	docker compose -f $(COMPOSE_FILE) up --build

clean:
	docker compose -f $(COMPOSE_FILE) down
	rm -rf ./config_test


# Build and push
build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):latest -t $(IMAGE_NAME):$(VERSION) .

push: build
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(VERSION)