# define configuration of AWS Terraform provider

provider "aws" {
  alias   = "main"
  region  = var.aws_region
}