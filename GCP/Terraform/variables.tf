variable "credentials" {
  description = "my GCP credentials file"
  default     = "~/.google/credentials/google_credentials.json"
}

variable "project" {
  description = "project id"
  default     = "terraform-demo-452020"
}

variable "region" {
  description = "region"
  default     = "us-central1"
}

variable "location" {
  description = "project location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "my BigQuery dataset name"
  default     = "de_dataset"
}

variable "gcs_bucket_name" {
  description = "my GCS bucket name"
  default     = "terraform-demo-452020-de_bucket"
}

variable "gcs_storage_class" {
  description = "bucket storage class"
  default     = "STANDARD"
}

##create a vm instance
variable "instance_name" {
  description = "instance name"
  default     = "test-instance-gcp"
}

variable "instance_type" {
  description = "instance type"
  default     = "e2-standard-4"
}

variable "instance_zone" {
  description = "instance zone"
  default     = "us-central1-c"
}

variable "account_id" {
  description = "service account id"
  default     = "230078498060-compute@developer.gserviceaccount.com"
}

variable "subnetwork" {
  description = "subnetwork"
  default     = "default"
}