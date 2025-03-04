.PHONY: setup start stop test clean seed-data format lint deploy

# Setup the project
setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -e .

# Start the application
start:
	. venv/bin/activate && uvicorn workspace.app:app --reload --host 0.0.0.0 --port 8000

# Stop the application (find and kill the process)
stop:
	pkill -f "uvicorn workspace.app:app" || echo "No running instance found"

# Run tests
test:
	. venv/bin/activate && pytest

# Clean up temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .coverage -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +

# Seed sample data
seed-data:
	. venv/bin/activate && python scripts/seed_data.py

# Format code
format:
	. venv/bin/activate && black workspace tests scripts

# Lint code
lint:
	. venv/bin/activate && flake8 workspace tests scripts

# Deploy the application
deploy:
	bash scripts/deploy.sh

# PhiData commands
phi-init:
	. venv/bin/activate && phi init

phi-start:
	. venv/bin/activate && phi start

phi-stop:
	. venv/bin/activate && phi stop

# Docker commands
docker-build:
	docker build -t reward-agent .

docker-run:
	docker run -p 8000:8000 -d --name reward-agent-api reward-agent

docker-test:
	docker run --rm reward-agent test

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down
