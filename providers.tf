terraform {
  required_version = ">= 1.4"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.63"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
