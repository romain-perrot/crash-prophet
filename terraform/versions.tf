# Define the configuration of Terraform itself

terraform {
  # I don't know the AWS provider is configured here again (it is already configured in ./aws.tf)
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.58"
    }
  }
  required_version = "~> 1.4"
}