resource "google_cloud_run_service_iam_member" "member" {
  project = google_cloud_run_service.default.project
  location = google_cloud_run_service.default.location
  service = google_cloud_run_service.default.name
  role = "roles/run.admin"
  member = "serviceAccount:${var.gcp_service_account}"
}

resource "google_cloud_run_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"

  template {
    spec {
      service_account_name = var.gcp_service_account
      containers {
        image = "europe-west4-docker.pkg.dev/gptunes-dev/gptunes-backend/gptunes-backend:${var.image_tag}"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
