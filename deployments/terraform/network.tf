variable "vpc_cidr_block" {
  description = "The top-level CIDR block for the VPC."
  default = "10.1.0.0/16"
}

variable "cidr_blocks" {
  description = "The CIDR blocks to create the workstations in."
  default = [
    "10.1.1.0/24",
    "10.1.2.0/24"]
}
#

resource "aws_vpc" "default" {
  cidr_block = "${var.vpc_cidr_block}"
  enable_dns_hostnames = true

  tags = {
    Name = "${var.app_name}"
  }
}

# Create an internet gateway to give our subnet access to the outside world
resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"

  tags = {
    Name = "${var.app_name}"
  }
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
  route_table_id = "${aws_vpc.default.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = "${aws_internet_gateway.default.id}"
}

# Grab the list of availability zones
data "aws_availability_zones" "available" {}

# Create a subnet to launch our instances into
resource "aws_subnet" "default" {
  count = "${length(var.cidr_blocks)}"
  vpc_id = "${aws_vpc.default.id}"
  availability_zone = "${data.aws_availability_zones.available.names[count.index]}"
  cidr_block = "${var.cidr_blocks[count.index]}"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}"
  }
}

resource "aws_security_group" "vpc-gw" {
  name = "vpce-sg-s3"
  description = "Security Group for S3 VPC Endpoint"
  vpc_id = "${aws_vpc.default.id}"

  # VPC 内からの接続を許可
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"

    cidr_blocks = [
      "${aws_vpc.default.cidr_block}",
    ]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      "${aws_vpc.default.cidr_block}",
    ]
  }
}

resource "aws_vpc_endpoint" "app" {
  vpc_id = "${aws_vpc.default.id}"
  service_name = "com.amazonaws.ap-northeast-1.transfer.server"
  vpc_endpoint_type = "Interface"

  # 先ほど作成した VPC エンドポイント用の SG を指定
  security_group_ids = [
    "${aws_security_group.vpc-gw.id}",
  ]

  subnet_ids = "${aws_subnet.default.*.id}"

  private_dns_enabled = true
}

output "vpc" {
  value = {
    vpc_id = "${aws_vpc.default.id}"
    subnet_dis = "${aws_subnet.default.*.id}"
  }
}