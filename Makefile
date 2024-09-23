dev: 
	docker compose  -f ./docker/docker-compose.dev.yml --env-file ./.env/.env up --build

down:
	docker-compose -f ./docker/docker-compose.dev.yml stop

test:
	pytest --cov=src --color=yes --ignore src tests

