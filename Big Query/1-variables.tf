variable "GCP_PROJECT" {
  description = "GCP Project ID"
  type        = string
  default     = "tcloud-sa-sandbox-1"
}

variable "GCP_REGION" {
  type    = string
  default = "asia-east1"
}

variable "bigquery_name" {
  type = string
  # bq 命名規則
  default = "martin-bq"
}

variable "bigquery_dataset_name" {
  type = string
  # bq 命名規則
  default = "martin-bq-dataset"
}
