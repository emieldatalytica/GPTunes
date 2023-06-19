#!/bin/bash

if [[ "$1" == "main" ]]; then
  BUCKET="terraform_bucket_emiel_prod"
else
  BUCKET="terraform_bucket_emiel"
fi

cat > backend.tf << EOF
terraform {
  backend "gcs" {
    bucket = "$BUCKET"
    prefix = "terraform/state"
  }
}
EOF
