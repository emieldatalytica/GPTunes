terraform {
  backend "gcs" {
    bucket = "terraform_bucket_emiel"
    prefix = "terraform/state"
  }
}
