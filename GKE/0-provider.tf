##################################################################################
# CONFIGURATION
##################################################################################
terraform {
  required_version = ">=1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.40.0"
    }
  }
}

##################################################################################
# PROVIDERS
##################################################################################
provider "google" {
  project     = var.GCP_PROJECT
  region      = var.GCP_REGION
  credentials = file("/Users/chenbowei/Downloads/cloud-sa-sandbox-1-532f072c4744.json") # 請將路徑替換為您的 GCP 服務帳戶(可以直接使用 GCE 的 SA -> 請妥善保存) JSON 憑證文件的路徑
  # zone        = var.zone
}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
  token                  = data.google_client_config.default.access_token
}
