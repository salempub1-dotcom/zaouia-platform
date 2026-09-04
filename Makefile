up:
	docker compose up --build
down:
	docker compose down
migrate:
	docker compose exec web python manage.py migrate
superuser:
	docker compose exec web python manage.py createsuperuser
test:
	docker compose exec web pytest -q
lint:
	ruff check .
