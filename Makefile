# Default to dev if not set
ENVIRONMENT ?= dev

.PHONY: ci backend frontend dependencies infra

# Load environment variables from the specified .env file (if it exists)
-include infra/envs/$(ENVIRONMENT)/.env
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
	docker build -t $(BACKEND_IMAGE_NAME) -f Dockerfile.backend \
	    --build-arg ENV_ID=$(ENV_ID) \
	    --build-arg OPENAI_API_KEY=$(OPENAI_API_KEY) \
	    .
	docker run -p 8080:8080 \
	    -v /Users/emieldeheij/Documents/GPTunes/infra/envs/dev:/ops \
		-e GOOGLE_APPLICATION_CREDENTIALS=$(SA_CREDENTIALS) \
	    $(BACKEND_IMAGE_NAME)

# Build and run the frontend with Docker locally
frontend:
	FRONTEND_IMAGE_NAME=gptunes-frontend
	hadolint --version
	hadolint Dockerfile.frontend
	docker build --build-arg DEBUG_MODE=$(DEBUG_MODE) -t $(FRONTEND_IMAGE_NAME) -f Dockerfile.frontend .
	docker run -p 8050:8050 $(FRONTEND_IMAGE_NAME)

# Compile and install updated dependencies
dependencies:
	pip-compile setup.cfg
	pip install -r requirements.txt

# Build GCP infrastructure with Terraform
infra:
	cd infra && \
		gcloud config set project $(ENV_NAME) && \
		terraform fmt && \
		tflint && \
		terraform init --backend-config="bucket=$(GCP_BUCKET_NAME)" --reconfigure && \
		terraform validate && \
		terraform plan -out tfplan -var-file=envs/$(ENVIRONMENT)/config.tfvars && \
		terraform apply tfplan
