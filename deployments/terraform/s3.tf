# S3

data "aws_iam_policy_document" "files" {
  version = "2012-10-17"
  statement {
    sid = "Vpce Allow"
    effect = "Deny"
    principals {
      type = "AWS"
      identifiers = [
        "${aws_iam_user.app.arn}"]
    }
    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::${var.app_name}",
      "arn:aws:s3:::${var.app_name}/*"
    ]
    condition {
      test = "StringNotEquals"
      variable = "aws:sourceVpce"
      values = [
        "${aws_vpc_endpoint.app.id}"
      ]
    }
  }
}

resource "aws_s3_bucket_public_access_block" "files" {
  bucket = "${aws_s3_bucket.files.id}"
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "files" {
  bucket = "${var.app_name}-files-${terraform.workspace}"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
      "https://localhost:18080",
      "http://${aws_alb.alb.dns_name}",
      "http://${aws_alb.alb.dns_name}/"
    ]
    expose_headers = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    Name = "${var.app_name}"
  }
}

data "aws_iam_policy_document" "log" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = ["arn:aws:iam::582318560864:root"]
    }
    actions = ["s3:PutObject"]
    resources = [
      "arn:aws:s3:::${var.app_name}-log-${terraform.workspace}",
      "arn:aws:s3:::${var.app_name}-log-${terraform.workspace}/*"
    ]
  }
}

resource "aws_s3_bucket_public_access_block" "log" {
  bucket = "${aws_s3_bucket.log.id}"
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "log" {
  bucket = "${var.app_name}-log-${terraform.workspace}"
  region = "${var.region}"

  policy = "${data.aws_iam_policy_document.log.json}"

  force_destroy = true

  tags = {
    Name = "${var.app_name}-log"
  }
}

output "s3" {
  value = {
    files_arn = "${aws_s3_bucket.files.arn}"
    files_bucket = "${aws_s3_bucket.files.bucket}"
  }
}