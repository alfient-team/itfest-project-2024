depl-build:
	@echo "Building Docker Image to dotpep/flaudlitefrontend..."
	
	@docker build -t dotpep/flaudlitefrontend .

depl-push:
	@echo "Pushing Docker Image to dotpep/flaudlitefrontend..."
	
	@docker push dotpep/flaudlitefrontend

run:
	@echo "Server npm is on running..."

	@npm run dev

install:
	@echo "Installing npm dependency..."

	@npm install

docker-build:
	@docker compose up --build -d

docker-run:
	@docker compose up -d

docker-logs:
	@docker compose logs -f

docker-down:
	@docker compose down
