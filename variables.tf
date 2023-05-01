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

variable "spotify_client_id_version" {
  description = "Spotify client ID version"
  type        = string
  default     = "cdc61e7993f04025a0be714ce2bd1760"
}

variable "spotify_client_secret_version" {
  type      = string
  default   = ""
  sensitive = true
}

variable "spotify_redirect_uri_version" {
  description = "Spotify redirect URI version"
  type        = string
  default     = "https://www.example.com/"
}
