variable "GCP_PROJECT" {
  description = "GCP Project ID"
  type        = string
  default     = "playground-s-11-58ee9325"
}

variable "GCP_REGION" {
  type    = string
  default = "us-central1"
}

variable "container_name" {
  type    = string
  default = "martin-cloud-run"
}
