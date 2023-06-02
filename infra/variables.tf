variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "europe-west4"
}

variable "gcp_project" {
  description = "GCP project"
  type        = string
  default     = "gptunes-dev"
}

variable "gcp_service_account" {
  description = "GCP service account"
  type        = string
  default     = ""
}
