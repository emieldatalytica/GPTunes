.PHONY: ci

## Format code using black and lint with flake8
ci:
	python -m isort --version
	python -m isort src
	python -m black --version
	python -m black src
	python -m flake8 --version
	python -m flake8 src --max-line-length=120

container:
	hadolint --version
	hadolint src/Dockerfile
	docker build -t playlist_generator src
	docker run -p 8080:8080 playlist_generator
