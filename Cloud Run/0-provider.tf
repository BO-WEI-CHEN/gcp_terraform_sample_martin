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
  credentials = file("/Users/chenbowei/Desktop/playground-s-11-58ee9325-845c538355a6.json")
  # zone        = var.zone
}
