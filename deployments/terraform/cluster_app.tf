// コンテナ
resource "aws_ecr_repository" "app" {
  name                 = "${var.app_name}/app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_ecr_repository" "nginx" {
  name                 = "${var.app_name}/nginx"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_security_group" "app" {
  name = "${var.app_name}-app"
  description = "APP SG"
  vpc_id = "${aws_vpc.default.id}"
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }
  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    security_groups = [
      "${aws_security_group.alb.id}"]
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
resource "aws_ecs_cluster" "default" {
  name = "${var.app_name}"
}

output "cluster_app" {
  value = {
    app_repo_url = "${aws_ecr_repository.app.repository_url}"
    nginx_repo_url = "${aws_ecr_repository.nginx.repository_url}"
    security_group_id = "${aws_security_group.app.id}"
    cluster_name = "${aws_ecs_cluster.default.name}"
  }
}

