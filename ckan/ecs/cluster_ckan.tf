// コンテナ
resource "aws_ecr_repository" "ckan_ckan" {
  name                 = "${var.app_name}/ckan/ckan"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_ecr_repository" "ckan_datapusher" {
  name                 = "${var.app_name}/ckan/datapusher"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_ecr_repository" "ckan_psql" {
  name                 = "${var.app_name}/ckan/postgresql"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_ecr_repository" "ckan_solr" {
  name                 = "${var.app_name}/ckan/solr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_efs_file_system" "ckan_data" {
  creation_token = "${var.app_name}/ckan-data"

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_efs_file_system" "ckan_psql_data" {
  creation_token = "${var.app_name}/ckan-psql-data"

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_efs_file_system" "ckan_solr_data" {
  creation_token = "${var.app_name}/ckan-solr-data"

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_efs_file_system" "ckan_redis_data" {
  creation_token = "${var.app_name}/ckan-redis-data"

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_efs_mount_target" "ckan_config_data" {
  count = "${length(aws_subnet.default.*)}"
  file_system_id = "${aws_efs_file_system.ckan_data.id}"
  subnet_id      = "${aws_subnet.default[count.index].id}"
}

resource "aws_efs_mount_target" "ckan_redis_data" {
  count = "${length(aws_subnet.default.*)}"
  file_system_id = "${aws_efs_file_system.ckan_redis_data.id}"
  subnet_id      = "${aws_subnet.default[count.index].id}"
}

resource "aws_efs_mount_target" "ckan_psql_data" {
  count = "${length(aws_subnet.default.*)}"
  file_system_id = "${aws_efs_file_system.ckan_psql_data.id}"
  subnet_id      = "${aws_subnet.default[count.index].id}"
}

resource "aws_efs_mount_target" "ckan_solr_data" {
  count = "${length(aws_subnet.default.*)}"
  file_system_id = "${aws_efs_file_system.ckan_solr_data.id}"
  subnet_id      = "${aws_subnet.default[count.index].id}"
}

resource "aws_security_group" "ckan" {
  name = "${var.app_name}-ckan"
  description = "CKAN SG"
  vpc_id = "${aws_vpc.default.id}"
  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }
  ingress {
    from_port = 5432
    to_port = 5432
    protocol = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}"
  }
}

# クラスタ
resource "aws_ecs_cluster" "ckan" {
  name = "${var.app_name}-ckan"
}


resource "aws_ssm_parameter" "ecr_ckan_psql_url" {
  name = "/${var.app_name}/systems/ckan/ecr_ckan_psql_url"
  type = "String"
  value = "${aws_ecr_repository.ckan_psql.repository_url}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ecr_ckan_solr_url" {
  name = "/${var.app_name}/systems/ckan/ecr_ckan_solr_url"
  type = "String"
  value = "${aws_ecr_repository.ckan_solr.repository_url}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_target_group_arn" {
  name = "/${var.app_name}/systems/ckan/target_group_arn"
  type = "String"
  value = "${aws_alb_target_group.ckan.arn}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_sequrity_group" {
  name = "/${var.app_name}/systems/ckan/sequrity_group_id"
  type = "String"
  value = "${aws_security_group.ckan.id}"
  key_id = "${aws_kms_key.default.key_id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_cluster_name" {
  name = "/${var.app_name}/systems/ckan/cluster_name"
  type = "String"
  value = "${aws_ecs_cluster.ckan.name}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "alb_url" {
  name = "/${var.app_name}/systems/alb_url"
  type = "String"
  value = "${aws_alb.alb.dns_name}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_data" {
  name = "/${var.app_name}/systems/ckan/data_id"
  type = "String"
  value = "${aws_efs_file_system.ckan_data.id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_psql_data" {
  name = "/${var.app_name}/systems/ckan/psql_data_id"
  type = "String"
  value = "${aws_efs_file_system.ckan_psql_data.id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_redis_data" {
  name = "/${var.app_name}/systems/ckan/redis_data_id"
  type = "String"
  value = "${aws_efs_file_system.ckan_redis_data.id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_ssm_parameter" "ckan_solr_data" {
  name = "/${var.app_name}/systems/ckan/solr_data_id"
  type = "String"
  value = "${aws_efs_file_system.ckan_solr_data.id}"

  tags = {
    Nmae = "${var.app_name}"
  }
}



resource "aws_alb_target_group" "ckan" {
  name = "${var.app_name}-ckan-tg"
  port = 5000
  protocol = "HTTP"
  vpc_id = "${aws_vpc.default.id}"
  target_type = "ip"

  health_check {
    interval = 60
    path = "/"
    protocol = "HTTP"
    timeout = 30
    healthy_threshold = 5
    unhealthy_threshold = 5
    matcher = 200
  }
}


// ckan
resource "aws_ssm_parameter" "ecr_ckan_ckan_url" {
  name = "/${var.app_name}/systems/ckan/ecr_ckan_ckan_url"
  type = "String"
  value = "${aws_ecr_repository.ckan_ckan.repository_url}"

  tags = {
    Nmae = "${var.app_name}"
  }
}

resource "aws_alb_listener" "ckan" {
  load_balancer_arn = "${aws_alb.alb.arn}"
  port = "5000"
  protocol = "HTTP"

  default_action {
    target_group_arn = "${aws_alb_target_group.ckan.arn}"
    type = "forward"
  }
}

output "cluster_ckan" {
  value = {
    ckan_ckan_repo_url = "${aws_ecr_repository.ckan_ckan.repository_url}"
    ckan_datapusher_repo_url = "${aws_ecr_repository.ckan_datapusher.repository_url}"
    ckan_psql_repo_url = "${aws_ecr_repository.ckan_psql.repository_url}"
    ckan_solr_repo_url = "${aws_ecr_repository.ckan_solr.repository_url}"
    ckan_security_group_id = "${aws_security_group.ckan.id}"
    ckan_cluster_name = "${aws_ecs_cluster.ckan.name}"
    ckan_config_data_id = "${aws_efs_file_system.ckan_data.id}"
    ckan_psql_data_id = "${aws_efs_file_system.ckan_psql_data.id}"
    ckan_redis_data_id = "${aws_efs_file_system.ckan_redis_data.id}"
    ckan_solr_data_id = "${aws_efs_file_system.ckan_solr_data.id}"
  }
}
