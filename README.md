# GPTunes
[![Auto-format and lint](https://github.com/emieldatalytica/GPTunes/actions/workflows/autoformat_and_lint.yml/badge.svg)](https://github.com/emieldatalytica/GPTunes/actions/workflows/autoformat_and_lint.yml)

[![Build Docker image and set up GCP infrastructure](https://github.com/emieldatalytica/GPTunes/actions/workflows/deploy_docker_image.yml/badge.svg)](https://github.com/emieldatalytica/GPTunes/actions/workflows/deploy_docker_image.yml)

This repository contains the code for the GPTunes application that allows you to generate themed playlists within a matter of seconds! To try it out, visit the following website: https://gptunes.nl/. Enjoy the music!

## General overview
GPTunes is hosted on Google Cloud Platform, where the frontend that users interact with and the backend are separately deployed as serverless Cloud Run services. The cloud resources are automatically rolled out by a CI/CD pipeline.

```mermaid
graph TD
    A[Github CI/CD Workflow] --> |Builds & tags with commit SHA| B[Docker Backend Image]
    A --> |Builds & tags with commit SHA| C[Docker Frontend Image]
    B -->|Pushed to| D[Backend Artifact Repository]
    C -->|Pushed to| E[Frontend Artifact Repository]
    D --> F{input var = SHA}
    E --> F
    F --> G[Terraform apply Cloud Run Module]
    G -->|Deploys| I[Cloud Run 'backend' service]
    G -->|Deploys| H[Cloud Run 'frontend' service]
    J[User] -.->|Sends theme to| I
    I -.->|Posts theme to| H
    H -.->|Compiles themed playlist and returns response| I
```
