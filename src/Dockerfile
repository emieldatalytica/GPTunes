# Docker image to run the FastAPI app from playlist_generator.py
FROM python:3.9-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/src

CMD ["uvicorn", "src.playlist_generator:playlist_generator", "--host", "0.0.0.0", "--port", "8080"]
