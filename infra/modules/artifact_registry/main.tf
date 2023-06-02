resource "google_artifact_registry_repository_iam_member" "member" {
  project = google_artifact_registry_repository.backend_image_repo.project
  location = google_artifact_registry_repository.backend_image_repo.location
  repository = google_artifact_registry_repository.backend_image_repo.name
  role = "roles/artifactregistry.admin"
  member = "serviceAccount:${var.gcp_service_account}"
}

resource "google_artifact_registry_repository" "backend_image_repo" {
  location      = "europe-west4"
  repository_id = "gptunes-backend"
  description   = "The GPTunes backend API image repository"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}
