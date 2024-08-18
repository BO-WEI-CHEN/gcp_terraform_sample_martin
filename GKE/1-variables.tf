variable "GCP_PROJECT" {
  description = "GCP Project ID"
  type        = string
  default     = "cloud-sa-sandbox-1"
}

variable "GCP_REGION" {
  type    = string
  default = "asia-east1"
}

variable "cluster_name" {
  type    = string
  default = "martin-iac-test"
}
