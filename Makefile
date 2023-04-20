.PHONY: ci container dependencies

# Format code using black and lint with flake8
ci:
	python -m isort --version
	python -m isort src
	python -m black --version
	python -m black src
	python -m flake8 --version
	python -m flake8 src --max-line-length=120

# Build and run the Docker container locally
container:
	hadolint --version
	hadolint src/Dockerfile
	docker build -t playlist_generator src
	docker run -p 8080:8080 playlist_generator

# Compile and install updated dependencies
dependencies:
	pip-compile setup.cfg
	pip install -r requirements.txt
