.PHONY: ci backend frontend dependencies infra

# Load environment variables from the dev .env file
-include infra/envs/dev/.env
export

# Format code using black and lint with flake8
ci:
	python -m isort --version
	python -m isort src
	python -m black --version
	python -m black src
	python -m flake8 --version
	python -m flake8 src --max-line-length=120
	python -m mypy --version
	python -m mypy src

# Build and run the backend with Docker locally
backend:
	hadolint --version
	hadolint Dockerfile.backend
	docker build -t $(BACKEND_IMAGE_NAME) -f Dockerfile.backend .
	docker run -p 8080:8080 \
		-v /Users/emieldeheij/Documents/GPTunes/infra/envs/dev:/ops \
		-e GOOGLE_APPLICATION_CREDENTIALS=$(SA_CREDENTIALS) \
		-e ENV_ID=$(ENV_ID) \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		$(BACKEND_IMAGE_NAME)

# Build and run the frontend with Docker locally
frontend:
	FRONTEND_IMAGE_NAME=gptunes-frontend
	hadolint --version
	hadolint Dockerfile.frontend
	docker build -t $(FRONTEND_IMAGE_NAME) -f Dockerfile.frontend .
	docker run -p 8050:8050 $(FRONTEND_IMAGE_NAME)


# Compile and install updated dependencies
dependencies:
	pip-compile setup.cfg
	pip install -r requirements.txt

# Build GCP infrastructure with Terraform
infra:
	cd infra && \
		terraform fmt && \
		tflint && \
		terraform init && \
		terraform validate && \
		terraform plan -out tfplan -var-file=envs/dev/config.tfvars && \
		terraform apply tfplan
