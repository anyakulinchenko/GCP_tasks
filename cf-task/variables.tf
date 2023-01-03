variable "project_id" {
  default     = "cf-task"
  type        = string
  description = "Project ID"
}

variable "region" {
  default     = "europe-central2"
  type        = string
  description = "Region"
}

variable "dataset_id" {
  default     = "task_cf_dataset"
  type        = string
  description = "Dataset"
}

variable "table_id" {
  default     = "task_cf_table"
  type        = string
  description = "Project ID to deploy resources in."
}

variable "force_destroy" {
  default = true
}

variable "deletion_protection" {
  default = false
}