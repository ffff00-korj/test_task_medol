run:
	poetry run python -m app.main

up_db:
	docker compose up -d --build

down_db:
	docker compose down
