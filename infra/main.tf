module "artifact_registry" {
  source              = "./modules/artifact_registry"
  gcp_service_account = var.gcp_service_account
}

module "cloud_run" {
  source = "./modules/cloud_run"
}
