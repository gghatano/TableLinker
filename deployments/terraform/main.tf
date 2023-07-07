#AWS Settings
//variable "access_key" {}
//variable "secret_key" {}
variable "region" {
  default = "ap-northeast-1"
}
variable "app_name" {}
variable "app_domain" {}

terraform {
  backend "s3" {
    bucket = "tablelinker-terraform-state"
    key = "tablelinker.terraform.tfstate"
    region = "ap-northeast-1"
    profile = "tablelinker"
  }
}

# provider
provider "aws" {
  version = "~> 2.1"
  region = "${var.region}"
  profile = "tablelinker"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
  profile = "tablelinker"
}

data "aws_caller_identity" "self" { }
