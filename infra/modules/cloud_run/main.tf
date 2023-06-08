resource "google_cloud_run_v2_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    spec {
      containers {
        name = "gptunes-backend"
        ports {
            container_port = 8080
        }
        image = "europe-west4-docker.pkg.dev/gptunes-dev/gptunes-backend/gptunes-backend:${var.image_tag}"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
