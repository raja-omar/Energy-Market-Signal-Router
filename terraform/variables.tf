variable "project_name" {
  type        = string
  default     = "energy-market-signal-router"
  description = "Project name for resource naming"
}

variable "redis_node_type" {
  type        = string
  default     = "cache.t3.micro"
  description = "ElastiCache node type (when using AWS)"
}

# Uncomment when enabling ElastiCache
# variable "subnet_ids" {
#   type        = list(string)
#   description = "VPC subnet IDs for Redis"
# }
# variable "security_group_ids" {
#   type        = list(string)
#   description = "Security group IDs for Redis"
# }
