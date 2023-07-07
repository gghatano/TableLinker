variable "ckan_instance_class" {
  default = "t2.medium"
}

resource "aws_security_group" "ckan2" {
  name = "${var.app_name}-ckan2"
  description = "Allow ssh"
  vpc_id = "${aws_vpc.default.id}"
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
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

resource "aws_instance" "ckan" {
  ami           = "${data.aws_ami.ubuntu-1604.id}"
  instance_type = "${var.ckan_instance_class}"
  key_name      = "${aws_key_pair.gateway.id}"

  subnet_id              = "${element(aws_subnet.default.*.id,0)}"
  vpc_security_group_ids = ["${aws_security_group.ckan2.id}"]
  user_data              = "${data.template_file.startup.rendered}"

  root_block_device {
    volume_type = "gp2"
    volume_size = "30"
  }

  monitoring = false

  tags = {
    Name = "${var.app_name}-ckan"
  }
}

resource "aws_eip" "ckan" {
  instance = "${aws_instance.ckan.id}"
  vpc = true
}

output "ckan" {
  value = {
    ipaddress = "${aws_eip.ckan.public_ip}"
  }
}