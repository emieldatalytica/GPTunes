.PHONY: ci container dependencies infra

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

# Build and run the Docker container locally
IMAGE_NAME = gptunes_dev
container:
	hadolint --version
	hadolint Dockerfile
	docker build -t $(IMAGE_NAME) .
	docker run -p 8080:8080 \
		-v /Users/emieldeheij/Documents/GPTunes/infra/envs/dev:/ops \
		-e GOOGLE_APPLICATION_CREDENTIALS=/ops/gptunes-dev-27118a274ad3.json \
		-e GPTUNES_DEV_ENV_ID=$(GPTUNES_DEV_ENV_ID) \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		$(IMAGE_NAME)


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
