variable "app_instance_class" {}

variable "public_key_path" {
  description = "Path to public key for ssh access"
  default     = "~/.ssh/id_rsa-tablelinker.pub"
}


# Get the list of official Canonical Ubuntu 16.04 AMIs
data "aws_ami" "ubuntu-1804" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Get the list of official Canonical Ubuntu 16.04 AMIs
data "aws_ami" "ubuntu-1604" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

data "template_file" "startup" {
  template = "${file("${path.module}/templates/startup.sh.tpl")}"
  vars = {
    region = "${var.region}"
    app_name = "${var.app_name}"
  }
}

resource "aws_security_group" "ssh" {
  name = "${var.app_name}-ssh"
  description = "Allow ssh"
  vpc_id = "${aws_vpc.default.id}"
  ingress {
    from_port = 22
    to_port = 22
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

# 作業用インスタンスキーペア
resource "aws_key_pair" "gateway" {
  key_name   = "${var.app_name}-gateway"
  public_key = "${file("${var.public_key_path}")}"
}

# 作業用インスタンス
resource "aws_instance" "gateway" {
  #ami           = "${data.aws_ami.ubuntu-1604.id}"
  ami = "ami-0df91b17a940f80a2"
  instance_type = "${var.app_instance_class}"
  key_name      = "${aws_key_pair.gateway.id}"

  subnet_id              = "${element(aws_subnet.default.*.id,0)}"
  vpc_security_group_ids = ["${aws_security_group.ssh.id}"]
  user_data              = "${data.template_file.startup.rendered}"

  root_block_device {
    volume_type = "gp2"
    volume_size = "30"
  }

  monitoring = false

  tags = {
    Name = "${var.app_name}"
  }
}

# 作業用インスタンスIPアドレス
resource "aws_eip" "web" {
  instance = "${aws_instance.gateway.id}"
  vpc = true
}

output "gateway" {
  value = {
    ipaddress = "${aws_eip.web.public_ip}"
    ssh = "ubuntu@${aws_eip.web.public_dns}"
  }
}