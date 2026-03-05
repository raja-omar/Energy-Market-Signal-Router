# Minimal Terraform config for Redis (ElastiCache-style)
# This demonstrates IaC; adjust provider and resources for your cloud.

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Example: ElastiCache Redis (uncomment and configure for AWS)
# resource "aws_elasticache_subnet_group" "redis" {
#   name       = var.project_name
#   subnet_ids = var.subnet_ids
# }
#
# resource "aws_elasticache_replication_group" "redis" {
#   replication_group_id = "${var.project_name}-redis"
#   node_type            = var.redis_node_type
#   num_cache_clusters   = 1
#   parameter_group_name = "default.redis7"
#   subnet_group_name    = aws_elasticache_subnet_group.redis.name
#   security_group_ids   = var.security_group_ids
# }
#
# output "redis_endpoint" {
#   value = aws_elasticache_replication_group.redis.primary_endpoint_address
# }

# Placeholder: outputs for local/docker usage
output "redis_host" {
  value       = "localhost"
  description = "Redis host (use with docker-compose for local dev)"
}

output "redis_port" {
  value       = 6379
  description = "Redis port"
}
