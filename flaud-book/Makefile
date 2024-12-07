depl-build:
	@echo "Building Docker Image to dotpep/flaudlitebackend..."
	
	@docker build -t dotpep/flaudlitebackend .

depl-push:
	@echo "Pushing Docker Image to dotpep/flaudlitebackend..."
	
	@docker push dotpep/flaudlitebackend

run:
	@echo "Server is on running..."

	@fastapi dev .\app\main.py

docker-build:
	@docker compose up --build -d

docker-run:
	@docker compose up -d

docker-logs:
	@docker compose logs -f

docker-down:
	@docker compose down

docker-remove:
	@docker compose down -v
	#@docker-compose down --remove-orphans

docker-exec-app:
	@docker exec -it fastapi_app sh

docker-exec-db:
	@docker exec -it postgres_db psql -U postgres -d app_db
	#@docker exec -it postgres_db sh

test:
	@echo "Testing..."
	@poetry pytest