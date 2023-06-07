resource "google_cloud_run_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"

  template {
    spec {
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
