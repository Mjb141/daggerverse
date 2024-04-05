terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Name = "Gitlab-Runner"
    }
  }
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/24"
}
