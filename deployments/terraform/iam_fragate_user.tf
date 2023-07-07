resource "aws_iam_user" "deployer" {
  name = "${var.app_name}-deployer"
}

resource "aws_iam_access_key" "deployer" {
  user = "${aws_iam_user.deployer.name}"
}

data "aws_iam_policy_document" "deployer" {

  statement {
    actions = [
      "kms:Decrypt"
    ]
    effect = "Allow"
    resources = ["${aws_kms_key.default.arn}"]
  }

  statement {
    effect = "Allow"
    actions = [
      "ssm:DescribeParameters",
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath",
    ]
    resources = [
      "arn:aws:ssm:${var.region}:${data.aws_caller_identity.self.account_id}:parameter/*"
    ]
  }

  statement {
    actions = [
      "s3:ListBucket"
    ]

    resources = [
      "${aws_s3_bucket.log.arn}"
    ]

    condition {
      test = "StringEquals"
      variable = "fragate"

      values = [
        ""
      ]
    }
  }

  statement {
    actions = [
      "s3:ListBucket",
    ]

    resources = [
      "${aws_s3_bucket.log.arn}",
    ]

    condition {
      test = "StringLike"
      variable = "s3:prefix"

      values = [
        "fragate",
        "fragate/*"
      ]
    }
  }

  statement {
    actions = [
      "s3:*",
    ]

    resources = [
      "${aws_s3_bucket.log.arn}/fragate",
    ]
  }
}

resource "aws_iam_policy" "deployer" {
  name = "${var.app_name}-policy"
  description = "${var.app_name} policy"
  policy = "${data.aws_iam_policy_document.deployer.json}"
}

resource "aws_iam_policy_attachment" "deployer" {
  name = "attachment"
  users = [
    "${aws_iam_user.deployer.id}"]
  roles = [
    "${aws_iam_role.fragate.id}"]
  policy_arn = "${aws_iam_policy.deployer.arn}"
}

resource "aws_iam_user_policy_attachment" "deployer2" {
  user = "${aws_iam_user.deployer.id}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

resource "aws_iam_user_policy_attachment" "deployer3" {
  user = "${aws_iam_user.deployer.id}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

output "iam_user_deployer" {
  value = {
    #encrypted_secret = "${aws_iam_access_key.deployer.encrypted_secret}"
    secret = "${aws_iam_access_key.deployer.secret}"
    key_id = "${aws_iam_access_key.deployer.id}"
    user = "${aws_iam_access_key.deployer.user}"
  }
}