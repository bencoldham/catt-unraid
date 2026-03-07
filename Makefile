# Dockerhub info
IMAGE_NAME = bencoldham/catt-unraid
VERSION = 0.0.1

# Testing/clean-up.
.PHONY: run clean
run:
	docker compose down
	rm -rf ./config_test
	mkdir ./config_test
	docker compose up --build

clean:
	docker compose down
	rm -rf ./config_test

# Build and push
build:
	docker build -t $(IMAGE_NAME):latest -t $(IMAGE_NAME):$(VERSION) .

push: build
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(VERSION)