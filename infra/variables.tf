variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "europe-west4"
}

variable "gcp_project" {
  description = "GCP project"
  type        = string
}

variable "gcp_service_account" {
  description = "GCP service account"
  type        = string
}

variable "image_tag" {
  description = "Image tag"
  type        = string
  default     = "latest"
}
