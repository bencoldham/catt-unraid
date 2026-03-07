.PHONY: run clean

run:
	docker compose down
	rm -rf ./config_test
	mkdir ./config_test
	docker compose up --build

clean:
	docker compose down
	rm -rf ./config_test