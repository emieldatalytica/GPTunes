# Docker image to run the FastAPI app from playlist_generator.py
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/ .

EXPOSE 8080

ARG ENV_ID
ENV ENV_ID=$ENV_ID
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

CMD ["uvicorn", "main:main", "--host", "0.0.0.0", "--port", "8080"]
