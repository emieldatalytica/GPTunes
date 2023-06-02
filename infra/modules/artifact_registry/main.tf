# resource "google_service_account" "service_account" {
#   account_id   = "tf-sa-${var.service_account_name}"
#   display_name = "Service Account for ${var.service_account_name}"
# }

# resource "google_project_iam_member" "iam_artifactregistryreader" {
#   role   = "roles/artifactregistry.manager"
#   member = "serviceAccount:${google_service_account.service_account.email}"
#   project = var.gcp_project
# }

resource "google_artifact_registry_repository_iam_member" "member" {
  project = google_artifact_registry_repository.backend_image_repo.project
  location = google_artifact_registry_repository.backend_image_repo.location
  repository = google_artifact_registry_repository.backend_image_repo.name
  role = "roles/artifactregistry.creator"
  member = "serviceAccount:${var.gcp_service_account}"
}

resource "google_artifact_registry_repository" "backend_image_repo" {
  location      = "europe-west4"
  repository_id = "gptunes_backend"
  description   = "The GPTunes backend API image repository"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}