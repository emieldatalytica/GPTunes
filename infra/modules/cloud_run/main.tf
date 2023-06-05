resource "google_cloud_run_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"

  template {
    spec {
      containers {
        image = "europe-west4-docker.pkg.dev/gptunes-dev/gptunes-backend/gptunes-backend"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
