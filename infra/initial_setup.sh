#!/bin/bash

# This script creates the initial setup for the project before you can get started with Terraform.
# Make sure to be logged in with your GCP account and to have the correct project selected (`gcloud auth login`)

# Parameter check
if [ "$1" != "dev" ] && [ "$1" != "main" ]; then
  echo "Invalid parameter. Use 'dev' or 'main'"
  exit 1
fi

# Load .env file
if [ "$1" = "dev" ]; then
  source envs/dev/.env
elif [ "$1" = "main" ]; then
  source envs/main/.env
fi

# Set the following variables to match your environment
PROJECT_ID="$ENV_NAME"
SERVICE_ACCOUNT_ID="$ENV_NAME"
SERVICE_ACCOUNT_DISPLAY_NAME="$ENV_NAME"
BUCKET_NAME="$GCP_BUCKET_NAME"

# Enable APIs
gcloud services enable iam.googleapis.com --project=$PROJECT_ID
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project=$PROJECT_ID
gcloud services enable run.googleapis.com --project=$PROJECT_ID

# Create the service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_ID \
    --description="Service Account for accessing Secret Manager secrets" \
    --display-name=$SERVICE_ACCOUNT_DISPLAY_NAME \
    --project=$PROJECT_ID

# Set output path for the JSON key file
if [ "$1" = "dev" ]; then
  OUTPUT_PATH="envs/dev/$SERVICE_ACCOUNT_ID.json"
elif [ "$1" = "main" ]; then
  OUTPUT_PATH="envs/main/$SERVICE_ACCOUNT_ID.json"
fi

# Create the JSON key file for the service account
gcloud iam service-accounts keys create $OUTPUT_PATH \
    --iam-account $SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --project=$PROJECT_ID

# Upload the JSON key file as a secret to Secret Manager
gcloud secrets create SA_CREDENTIALS \
    --replication-policy="automatic" \
    --data-file=$SERVICE_ACCOUNT_ID.json \
    --project=$PROJECT_ID

# Give the service account the role to access secrets
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# Give the service account the role to write to Artifact Registry
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/artifactregistry.writer

# Give the service account the role to access the Storage bucket
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/storage.admin

# Create 'gptunes-backend' repository
gcloud artifacts repositories create gptunes-backend \
    --repository-format=docker \
    --location=europe-west4 \
    --project=$PROJECT_ID

# Create 'gptunes-frontend' repository
gcloud artifacts repositories create gptunes-frontend \
    --repository-format=docker \
    --location=europe-west4 \
    --project=$PROJECT_ID

# Create a bucket to store the Terraform state remotely
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME
