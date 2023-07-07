// ロードバランサーの設定
resource "aws_security_group" "alb" {
  name = "${var.app_name}-alb"
  description = "ALB SG"
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
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
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

resource "aws_alb" "alb" {
  name = "${var.app_name}"
  security_groups = [
    "${aws_security_group.alb.id}"]
  subnets = "${aws_subnet.default.*.id}"
  internal = false
  enable_deletion_protection = false

  access_logs {
    bucket = "${aws_s3_bucket.log.bucket}"
    prefix = "alb/alb-"
    enabled = true
  }
}

// albのターゲットグループ
resource "aws_alb_target_group" "alb" {
  name = "${var.app_name}-tg"
  port = 80
  protocol = "HTTP"
  vpc_id = "${aws_vpc.default.id}"
  target_type = "ip"

  health_check {
    interval = 60
    path = "/status"
    protocol = "HTTP"
    timeout = 30
    healthy_threshold = 5
    unhealthy_threshold = 5
    matcher = 200
  }
}

//// 443ポートの設定。今回は事前にAWS Certificate Managerで作成済みの証明書を設定。
//resource "aws_alb_listener" "alb_443" {
//  load_balancer_arn = "${aws_alb.alb.arn}"
//  port              = "443"
//  protocol          = "HTTPS"
//  ssl_policy        = "ELBSecurityPolicy-2015-05"
//  certificate_arn   = "${var.alb_certificate_arn}"
//
//  default_action {
//    target_group_arn = "${aws_alb_target_group.alb.arn}"
//    type             = "forward"
//  }
//}

resource "aws_alb_listener" "alb" {
  load_balancer_arn = "${aws_alb.alb.arn}"
  port = "80"
  protocol = "HTTP"

  default_action {
    target_group_arn = "${aws_alb_target_group.alb.arn}"
    type = "forward"
  }
}

output "alb" {
  value = {
    dns_name = "${aws_alb.alb.dns_name}"
    arn = "${aws_alb.alb.arn}"
    target_group_arn = "${aws_alb_target_group.alb.arn}"
  }
}

//resource "aws_acm_certificate" "alb" {
//  domain_name = "${var.app_domain}"
//  validation_method = "DNS"
//
//  lifecycle {
//    create_before_destroy = true
//  }
//}

//variable "alb_certificate_arn" {
//  default = ""
//}
