output "coordinator_public_ip" {
  description = "Public IP of the Coordinator"
  value       = aws_instance.coordinator.public_ip
}

output "shards_public_ips" {
  description = "Public IPs of the Shards"
  value       = aws_instance.shards[*].public_ip
}