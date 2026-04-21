provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "coordinator" {
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t3.micro"
  vpc_security_group_ids = [aws_security_group.laba_sg.id]
  tags = { Name = "Sharding-Coordinator" }
}

resource "aws_instance" "shards" {
  count         = 2
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t3.micro"
  vpc_security_group_ids = [aws_security_group.laba_sg.id]
  tags = { Name = "Shard-Node-${count.index + 1}" }
}