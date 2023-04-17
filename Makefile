.PHONY: ci

## Format code using black and lint with flake8
ci:
	python -m black --version
	python -m black src
	python -m flake8 --version
	python -m flake8 src
