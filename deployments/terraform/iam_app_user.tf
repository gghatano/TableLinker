resource "aws_iam_user" "app" {
  name = "${var.app_name}-app"
  path = "/${var.app_name}/"

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_iam_access_key" "app" {
  user = "${aws_iam_user.app.name}"
}

resource "aws_iam_user_policy" "app" {
  name = "${var.app_name}-app"
  user = "${aws_iam_user.app.name}"

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "SendSES",
        "Effect": "Allow",
        "Action": [
          "ses:SendEmail",
          "ses:SendRawEmail",
          "ses:GetSendQuota"
        ],
        "Resource": "*"
      },
      {
        "Sid": "GETParams",
        "Effect": "Allow",
        "Action": [
          "ssm:GetParameters",
          "ssm:GetParametersByPath",
          "secretsmanager:GetSecretValue"
        ],
        "Resource": "*"
      },
      {
          "Sid": "S3",
          "Effect": "Allow",
          "Action": [
              "s3:PutObject",
              "s3:GetObject",
              "s3:PutObjectAcl",
              "s3:ListBucket",
              "s3:DeleteObject",
              "s3:GetBucketLocation"
          ],
          "Resource": [
              "${aws_s3_bucket.files.arn}",
              "${aws_s3_bucket.files.arn}/*"
          ]
      }
    ]
  }
  EOF
}

output "iam_user_app" {
  value = {
    #encrypted_secret = "${aws_iam_access_key.app.encrypted_secret}"
    secret = "${aws_iam_access_key.app.secret}"
    key_id = "${aws_iam_access_key.app.id}"
    user = "${aws_iam_access_key.app.user}"
  }
}