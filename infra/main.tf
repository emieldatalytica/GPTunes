module "cloud_run" {
  source      = "./modules/cloud_run"
  gcp_project = var.gcp_project
  image_tag   = var.image_tag
}
