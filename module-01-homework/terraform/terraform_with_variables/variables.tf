variable "credentials" {
  description = "My Credentials"
  default     = "/home/jaypatel/projects/Data Engineering/Data-Engineering-Zoomcamp-Homework/module-01-homework/terraform/keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "dtc-de-course-412115"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "demo_dataset_jp"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "terraform-demo-terra-bucket-jp"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}