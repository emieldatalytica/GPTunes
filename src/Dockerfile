# Docker image to run the FastAPI app from playlist_generator.py
FROM python:3.9-slim-buster

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.playlist_generator:app", "--host", "0.0.0.0", "--port", "8080"]
