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

variable "cf_dataset_id" {
  default     = "task_cf_dataset"
  type        = string
  description = "Dataset"
}

variable "df_dataset_id" {
  default     = "task_df_dataset"
  type        = string
  description = "Dataset"
}

variable "table_id" {
  default     = "task_cf_table"
  type        = string
  description = "BigQuery Table"
}

variable "output_table_success_messages" {
  default     = "output_table_success_messages"
  type        = string
  description = "BigQuery Table"
}

variable "output_table_error_messages" {
  default     = "output_table_error_messages"
  type        = string
  description = "BigQuery Table"
}

variable "pubsub_topic_name" {
  default = "cf_pubsub_topic"
  type = string
}

variable "subscription_name" {
  default = "cf_pubsub_subs1"
  type = string
}
