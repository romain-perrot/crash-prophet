# Define the possible variables that can be configured for this Terraform module

variable "project_name" {
  type    = string
  default = "pink-twins"
}

variable "environment" {
  type    = string
}

variable "aws_region" {
  type    = string
  default = "eu-west-2" # London
}

variable "image_folder" {
	type = string
	default = "satellite-images"
}
