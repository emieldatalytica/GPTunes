resource "google_service_account" "gptunes_sa" {
  account_id   = "gptunes-cloudrun"
  display_name = "gptunes-cloudrun"
  project      = var.gcp_project
}

resource "google_project_iam_member" "gptunes_sa_secrets_accessor" {
  project = var.gcp_project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.gptunes_sa.email}"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.gptunes_sa.email
    containers {
      name = "gptunes-backend"
      ports {
        container_port = 8080
      }
      image = "europe-west4-docker.pkg.dev/${var.gcp_project}/gptunes-backend/gptunes-backend:${var.image_tag}"
    }
  }
}
