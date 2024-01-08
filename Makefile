dev: 
	sudo docker-compose  -f ./docker/docker-compose.dev.yml up --build &
	ngrok http --domain=honestly-assured-wildcat.ngrok-free.app --log=stdout 8080 > /dev/null

down:
	docker-compose -f ./docker/docker-compose.dev.yml stop

test:
	pytest --cov=src --color=yes --ignore src tests

