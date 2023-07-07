resource "aws_kms_key" "default" {
  description = "KMS key for ssm"
  deletion_window_in_days = 10
}

resource "aws_ssm_parameter" "app_name" {
  name = "/${var.app_name}/app_name"
  description = "App Name"
  type = "String"
  value = "${var.app_name}"

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "app_domain" {
  name = "/${var.app_name}/app_domain"
  description = "App Domain"
  type = "String"
  value = "${var.app_domain}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "bucket_name" {
  name = "/${var.app_name}/bucket_name"
  description = "Bucket Name"
  type = "SecureString"
  value = "${aws_s3_bucket.files.bucket}"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "db_host" {
  name = "/${var.app_name}/db_host"
  description = "DB Host"
  type = "SecureString"
  value = "${aws_db_instance.default.address}"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "db_name" {
  name = "/${var.app_name}/db_name"
  description = "DB Name"
  type = "SecureString"
  value = "${var.db_name}"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "db_user" {
  name = "/${var.app_name}/db_user"
  type = "SecureString"
  value = "${var.db_username}"
  overwrite = true
  key_id = "${aws_kms_key.default.key_id}"
  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "db_pass" {
  name = "/${var.app_name}/db_pass"
  type = "SecureString"
  value = "${var.db_password}"
  key_id = "${aws_kms_key.default.key_id}"
  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "redis_endpoint" {
  name = "/${var.app_name}/redis_endpoint"
  type = "SecureString"
  value = "redis://${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "broker_endpoint" {
  name = "/${var.app_name}/broker_endpoint"
  type = "SecureString"
  value = "redis://${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}/1"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "result_backend_endpoint" {
  name = "/${var.app_name}/result_backend_endpoint"
  type = "SecureString"
  value = "redis://${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}/2"
  key_id = "${aws_kms_key.default.key_id}"
  overwrite = true

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "app_user_key_id" {
  name = "/${var.app_name}/app_user_key_id"
  type = "SecureString"
  value = "${aws_iam_access_key.app.id}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "app_user_secret" {
  name = "/${var.app_name}/app_user_secret"
  type = "SecureString"
  value = "${aws_iam_access_key.app.secret}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "app_user" {
  name = "/${var.app_name}/app_user"
  type = "SecureString"
  value = "${aws_iam_access_key.app.user}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

##
## For deploy

resource "aws_ssm_parameter" "ecr_nginx_url" {
  name = "/${var.app_name}/systems/ecr_nginx_url"
  type = "SecureString"
  value = "${aws_ecr_repository.nginx.repository_url}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}


resource "aws_ssm_parameter" "ecr_app_url" {
  name = "/${var.app_name}/systems/ecr_app_url"
  type = "SecureString"
  value = "${aws_ecr_repository.app.repository_url}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}
resource "aws_ssm_parameter" "ecr_cluster_name" {
  name = "/${var.app_name}/systems/ecr_cluster_name"
  description = "App Name"
  type = "String"
  value = "${aws_ecs_cluster.default.name}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "target_group_arn" {
  name = "/${var.app_name}/systems/target_group_arn"
  type = "SecureString"
  value = "${aws_alb_target_group.alb.arn}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "sequrity_group" {
  name = "/${var.app_name}/systems/sequrity_group_id"
  type = "SecureString"
  value = "${aws_security_group.app.id}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "subnet_ids_0" {
  name = "/${var.app_name}/systems/subnet_ids_0"
  type = "SecureString"
  value = "${aws_subnet.default.0.id}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "subnet_ids_1" {
  name = "/${var.app_name}/systems/subnet_ids_1"
  type = "SecureString"
  value = "${aws_subnet.default.1.id}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ssm_parameter_arn_prefix" {
  name = "/${var.app_name}/systems/ssm_parameter_arn_prefix"
  type = "SecureString"
  value = "arn:aws:ssm:${var.region}:${data.aws_caller_identity.self.account_id}:parameter/${var.app_name}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ecs_execute_task_role_arn" {
  name = "/${var.app_name}/systems/ecs_execute_task_role_arn"
  type = "SecureString"
  value = "${aws_iam_role.fragate-execution.arn}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ecs_task_role_arn" {
  name = "/${var.app_name}/systems/ecs_task_role_arn"
  type = "SecureString"
  value = "${aws_iam_role.fragate.arn}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

