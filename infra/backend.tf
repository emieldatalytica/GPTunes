terraform {
  backend "gcs" {
    bucket = "terraform_bucket_emiel_prod"
    prefix = "terraform/state"
  }
}
