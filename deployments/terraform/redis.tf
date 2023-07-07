resource "aws_security_group" "redis" {
  name_prefix = "${var.app_name}"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 6379
    to_port = 6379
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

resource "aws_elasticache_subnet_group" "default" {
  name = "${var.app_name}-cache-subnet"
  subnet_ids = "${aws_subnet.default.*.id}"
}

resource "aws_elasticache_cluster" "default" {
  cluster_id = "cluster-redis"
  engine = "redis"
  engine_version = "5.0.6"
  node_type = "cache.t2.micro"
  port = 6379
  num_cache_nodes = 1
  parameter_group_name = "default.redis5.0"

  subnet_group_name = "${aws_elasticache_subnet_group.default.name}"
  security_group_ids  = [
    "${aws_security_group.redis.id}"
  ]

  tags = {
    Name = "${var.app_name}"
  }
}
output "redis_endpoint_addresses" {
  value = {
    endopoint = "${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}"
    broker_endpoint = "${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}/1"
    result_backend_endpoint = "${aws_elasticache_cluster.default.cache_nodes.0.address}:${aws_elasticache_cluster.default.cache_nodes.0.port}/2"
  }
}

// Cluster
//resource "aws_elasticache_replication_group" "default" {
//  replication_group_id = "${var.app_name}-redis-cluster"
//  replication_group_description = "Redis cluster for Hashicorp ElastiCache example"
//
//  node_type = "cache.t2.micro"
//  port = 6379
//  engine               = "redis"
//  engine_version       = "5.0.6"
//  parameter_group_name = "default.redis5.0.cluster.on"
//
//  snapshot_retention_limit = 5
//  snapshot_window = "00:00-05:00"
//
//  subnet_group_name = "${aws_elasticache_subnet_group.default.name}"
//  automatic_failover_enabled = true
//
//  cluster_mode {
//    replicas_per_node_group = 1
//    num_node_groups = "1"
//  }
//}
//
//output "configuration_endpoint_address" {
//  value = "${aws_elasticache_replication_group.default.configuration_endpoint_address}"
//  value = {
//    endopoint = "${aws_elasticache_replication_group.default.configuration_endpoint_address}"
//    broker_endpoint = "${aws_elasticache_replication_group.default.configuration_endpoint_address}/1"
//    result_backend_endpoint = "${aws_elasticache_replication_group.default.configuration_endpoint_addresss}/2"
//  }
//}
