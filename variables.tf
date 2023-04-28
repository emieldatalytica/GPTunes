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

variable "spotify_credentials_id_version" {
  description = "Spotify credentials ID version"
  type        = string
  default     = "cdc61e7993f04025a0be714ce2bd1760"
}

variable "spotify_redirect_uri_version" {
  description = "Spotify redirect URI version"
  type        = string
  default     = "https://www.example.com/"
}
