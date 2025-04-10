terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.94.1"
    }
  }
}

provider "aws" {
  # Configuration options
  region                   = var.aws_region
  shared_credentials_files = ["C:/Users/xin/.aws/credentials/aws.ini"]
  profile                  = "default"
}

resource "aws_s3_bucket" "de_test_vm_2025" {
  bucket = "de-test-vm-2025"

}

resource "aws_s3_object" "csv_file" {
  bucket = aws_s3_bucket.de_test_vm_2025.bucket
  key    = "csv_file/"
}

resource "aws_s3_object" "sql_file" {
  bucket = aws_s3_bucket.de_test_vm_2025.bucket
  key    = "sql_file/"
}