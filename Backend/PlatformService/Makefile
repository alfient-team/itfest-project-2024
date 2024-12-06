depl-build:
	@echo "Building Docker Image to dotpep/platformservicedotnet..."
	
	@docker build -t dotpep/platformservicedotnet .

depl-push:
	@echo "Pushing Docker Image to dotpep/platformservicedotnet..."
	
	@docker push dotpep/platformservicedotnet

depl-run:
	@echo "Running Docker Image in Localhost..."
	
	@docker run -p 8080:80 dotpep/platformservicedotnet

version:
	@echo "Current Version of Dotnet:"
	
	@dotnet --version

build:
	@echo "Building..."
	
	@dotnet build

run:
	@echo "Server is on running..."

	@dotnet run

# https-clean-trust
dev-certs:
	@echo "Cleaning..."
	@dotnet dev-certs https --clean
	@dotnet dev-certs https --trust

#docker-run:
#	@docker compose up --build -d

#docker-logs:
#	@docker compose logs -f

#docker-down:
#	@docker compose down

#test:
#	@echo "Testing..."
#	@dotnet test
