build:
	docker-compose build

up:
	docker-compose up -d web db

down:
	docker-compose down

reload:
	docker-compose exec web touch /tmp/reload.trigger

bash:
	docker-compose run --rm web bash

migrate:
	docker-compose run --rm web \
	bash -c ' \
		python3 -c "from db import create, drop; drop(); create()" \
	'
