variable "db_instance_class" {}
variable "db_name" {}
variable "db_username" {}
variable "db_password" {}
variable "db_protection" {
  type= bool
  default = false
}

resource "aws_db_subnet_group" "default" {
  name = "${var.app_name}-rds-subnet"
  description = "${var.app_name}"
  subnet_ids = "${aws_subnet.default.*.id}"
  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_security_group" "postgres" {
  name = "${var.app_name}-postgres"
  description = "for postgres"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 5432
    to_port = 5432
    protocol = "tcp"
    cidr_blocks = [
      "${var.vpc_cidr_block}"
    ]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_db_parameter_group" "postgres" {
  name = "${var.app_name}-postgres"
  family = "postgres10"
  description = "${var.app_name}-postgres"

  parameter {
    name = "log_min_duration_statement"
    value = "100"
  }

  //    parameter {
  //      name = "time_zone"
  //      value = "Asia/Tokyo"
  //    }
}

resource "random_id" "db-suffix" {
  byte_length = 4
}

resource "aws_db_instance" "default" {
  identifier = "${var.app_name}-${random_id.db-suffix.hex}"
  allocated_storage = 10
  engine = "postgres"
  engine_version = "10.13"
  storage_type = "gp2"
  instance_class = "${var.db_instance_class}"
  name = "${var.db_name}"

  deletion_protection = "${var.db_protection}"

  username = "${var.db_username}"
  password = "${var.db_password}"
  db_subnet_group_name = "${aws_db_subnet_group.default.name}"
  vpc_security_group_ids = [
    "${aws_security_group.postgres.id}"]
  parameter_group_name = "${aws_db_parameter_group.postgres.name}"
  multi_az = false
  publicly_accessible = false
  backup_retention_period = 7
  backup_window = "00:00-05:00"
  apply_immediately = "true"
  auto_minor_version_upgrade = "true"
  skip_final_snapshot = "true"
  tags = {
    Name = "${var.app_name}"
  }
}

output "rds_endpoint" {
  value = {
    db_host = "${aws_db_instance.default.address}"
    db_user = "${var.db_username}"
    db_password = "${var.db_password}"
  }
}
