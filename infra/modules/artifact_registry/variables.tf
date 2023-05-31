# variable "service_account_name" {
#   description = "GCP service account name for the artifact registry"
#   type        = string
#   default     = "artifact-registry"
# }

# variable "gcp_project" {
#   description = "GCP project"
#   type        = string
#   default     = "gptunes-dev"
# }

variable "gcp_service_account" {
  description = "GCP service account"
  type        = string
  default     = "gptunes-dev@gptunes-dev.iam.gserviceaccount.com"
}
