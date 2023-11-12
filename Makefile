dev: 
	docker-compose  -f ./docker-compose.dev.yml up --build

down:
	docker-compose -f ./docker-compose.dev.yml stop

test:
	pytest --cov=src --color=yes --ignore src tests

