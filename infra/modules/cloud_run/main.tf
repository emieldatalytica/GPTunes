resource "google_cloud_run_v2_service_iam_member" "member" {
  project = google_cloud_run_v2_service.default.project
  location = google_cloud_run_v2_service.default.location
  name = google_cloud_run_v2_service.default.name
  role = "roles/run.admin"
  member = "serviceAccount:${var.gcp_service_account}"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "gptunes-api"
  location = "europe-west4"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
      containers {
        name = "gptunes-backend"
        ports {
            container_port = 8080
        }
        image = "europe-west4-docker.pkg.dev/gptunes-dev/gptunes-backend/gptunes-backend:${var.image_tag}"
      }
  }
}
