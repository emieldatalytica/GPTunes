module "artifact_registry" {
  source              = "./modules/artifact_registry"
  gcp_service_account = var.gcp_service_account
}

module "cloud_run" {
  source      = "./modules/cloud_run"
  gcp_project = var.gcp_project
  image_tag   = var.image_tag
}
